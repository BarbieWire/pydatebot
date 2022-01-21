from dotenv import load_dotenv
import os

from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from menus.main_menu import MAIN_MENU
from menus.profile_menu import PROFILE_MENU, CREATE_NEW_MENU
from menus.search_menu import SEARCH_MENU, ALARM_MENU, LIKE_MENU
from database.db_control import DatabaseControl, DatabaseConnection
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from messages.cache_storage import CacheStorage


load_dotenv()
HOST, DATABASE, USER, PASSWORD = os.getenv("HOST"), os.getenv("DATABASE"), os.getenv("USER"), os.getenv("PASSWORD")


_storage = CacheStorage()
_conn = DatabaseConnection(host=HOST, database=DATABASE, user=USER, password=PASSWORD).connect()
_base = DatabaseControl(_conn)


class Search(StatesGroup):
    search = State()


async def show_profile(message: Message):
    chat_id = message.from_user.id

    if message.text == "My profile 👤":
        current = _base.get_user(message.from_user.id)

        if current is not None:
            await message.answer(text="Here's your form:", reply_markup=PROFILE_MENU)
            await bot.send_photo(caption=F"{current[4]}, {current[7]}, {current[2]}\n{current[6]}",
                                 photo=current[1],
                                 reply_markup=PROFILE_MENU,
                                 chat_id=message.from_user.id)
        else:
            await message.answer(text="You have no form ❌\nBut you still might create one", reply_markup=CREATE_NEW_MENU)

    elif message.text == "Back to main menu 🔙":
        await message.answer(text="Turning you back", reply_markup=MAIN_MENU)
        try:
            await _storage.delete_user(chat_id=chat_id)
        except Exception as _ex:
            pass

    elif message.text in ("Search 🔎", "Who's this?", "dislike", "like", "Ok"):
        if message.text in ["dislike", "like"]:
            await message.answer(text="form expired", reply_markup=MAIN_MENU)
        try:
            await _storage.delete_user(chat_id=chat_id)
        except Exception as ex:
            print(f"No user has been found {ex}")

        await Search.search.set()
        params = _base.get_user(chat_id)

        search_forms = _base.search(params[0], params[2], params[7], params[5], params[3])
        like_forms = _base.liked(chat_id)
        likes = []
        for i in like_forms:
            likes.append(_base.get_user(i))
        mutual_forms = _base.get_mutual(chat_id)
        mutual = []
        for i in mutual_forms:
            mutual.append(_base.get_user(i))

        await _storage.add(chat_id=message.from_user.id, forms=search_forms, likes=likes, mutual=mutual)
        await bot.send_message(text="Remember people can impersonate others!", reply_markup=ALARM_MENU, chat_id=message.from_user.id)


async def forming(user, chat_id, reply_markup=SEARCH_MENU):
    await bot.send_photo(caption=F"{user[4]}, {user[7]}, {user[2]}\n{user[6]}",
                         photo=user[1],
                         chat_id=chat_id,
                         reply_markup=reply_markup)


async def search(message: Message, state: FSMContext):
        user = await _storage.get_user(chat_id=message.from_user.id)
        if message.text == "Back to main menu 🔙":
            await state.finish()
            await message.answer(text="Turning you back", reply_markup=MAIN_MENU)

        elif message.text in ["like", "dislike"]:
            if message.text == "like":
                if user["likes"] != []:
                    _base.set_mutual(liker=user["likes"][0][0], liked=message.from_user.id)
                    await bot.send_message(chat_id=user["likes"][0][0], reply_markup=LIKE_MENU,
                                           text="Someone is interested in you...")

                    await message.answer(text=f"Mutual sympathy, link ---> [{user['likes'][0][4]}](tg://user?id={user['likes'][0][0]})", parse_mode="Markdown")
                    await forming(user=user["likes"][0], chat_id=message.from_user.id, reply_markup=None)
                    await _storage.delete_position(chat_id=message.from_user.id, dictionary="likes")
                else:
                    _base.like(liker=message.from_user.id, liked=user["forms"][0][0])
                    await bot.send_message(chat_id=user["forms"][0][0], reply_markup=LIKE_MENU,
                                           text="Someone is interested in you...")
                    await _storage.delete_position(chat_id=message.from_user.id, dictionary="forms")
            else:
                await _storage.delete_position(chat_id=message.from_user.id, dictionary="forms")

            try:
                if user["likes"] != []:
                    await message.answer(text="Your form liked by:")
                    await forming(user["likes"][0], chat_id=message.from_user.id)
                else:
                    await forming(user["forms"][0], chat_id=message.from_user.id)
            except Exception as _ex:
                await message.answer("Unfortunately here's no one... Come back later", reply_markup=MAIN_MENU)
                await state.finish()

        elif message.text in ["Who's this?", "Ok"]:
            if user["likes"] != []:
                await message.answer(text="Your form liked by:")
                await forming(user["likes"][0], message.from_user.id)
            elif user["likes"] == [] and user["mutual"] != []:
                for i in user["mutual"]:
                    await message.answer(text=f"Mutual sympathy, link ---> [{i[4]}](tg://user?id={user['mutual'][0][0]})", parse_mode="Markdown")
                    await forming(user=i, chat_id=message.from_user.id)
                    _base.delete_sympathy(liked=message.from_user.id, liker=i[0])
                await forming(user["forms"][0], message.from_user.id)
            else:
                await forming(user["forms"][0], message.from_user.id)


def main_menu_response_handler():
    dp.register_message_handler(show_profile, Text(equals=[
        "My profile 👤", "Back to main menu 🔙", "Search 🔎", "Who's this?", "dislike", "like", "Ok"
    ], ignore_case=False), state=None)
    dp.register_message_handler(search, content_types=["any"], state=Search.search)
