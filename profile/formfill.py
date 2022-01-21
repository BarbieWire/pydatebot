from loader import dp, bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from menus.profile_menu import PROFILE_MENU, GENDER_MENU, CANCEL, PREFERENCE_MENU
from database.db_control import DatabaseControl, DatabaseConnection
from menus.main_menu import DISABLE_MENU, TURN_BACK_MENU, MAIN_MENU
from dotenv import load_dotenv
import os


# VARIABLES
load_dotenv(".env")
HOST, DATABASE, USER, PASSWORD = os.getenv("HOST"), os.getenv("DATABASE"), os.getenv("USER"), os.getenv("PASSWORD")


_conn = DatabaseConnection(host=HOST, database=DATABASE, user=USER, password=PASSWORD).connect()


# Forming mutual form to send
async def forming(text, connection, message):
    show = DatabaseControl(connection).get_user(chat_id=int(message.from_user.id))
    await message.answer(text=f"{text}", reply_markup=PROFILE_MENU)
    await bot.send_photo(caption=F"{show[4]}, {show[7]}, {show[2]}\n{show[6]}",
                         photo=show[1],
                         reply_markup=PROFILE_MENU,
                         chat_id=message.from_user.id)


class FSMRegister(StatesGroup):
    photo = State()
    city = State()
    gender = State()
    name = State()
    preference = State()
    about = State()
    age = State()


async def initialization(message: Message):
    await FSMRegister.photo.set()
    await message.answer(text="send me a photo", reply_markup=CANCEL)


async def photo(message: Message, state: FSMContext):
    if message.content_type != 'photo':
        await message.answer(text="Please send me a photo")

    else:
        async with state.proxy() as data:
            data["chat_id"] = int(message.from_user.id)
            data["photo"] = message.photo[0].file_id

        await message.answer(text="Send me your city")
        await FSMRegister.next()


async def city(message: Message, state: FSMContext):
    if message.content_type == "text" and len(message.text) in range(3, 20):
        async with state.proxy() as data:
            data["City"] = message.text.capitalize()
        await message.answer(text="Now send me your gender", reply_markup=GENDER_MENU)
        await FSMRegister.next()

    else:
        if message.content_type != "text":
            await message.answer(text="Please, send me your city")
        else:
            await message.answer(text="Send me a real city")


async def gender(message: Message, state: FSMContext):
    if message.content_type == "text" and (message.text == "Male" or message.text == "Female"):
        async with state.proxy() as data:
            data["gender"] = message.text
        await message.answer(text="Now send me your name", reply_markup=ReplyKeyboardRemove())
        await FSMRegister.next()
    else:
        await message.answer(text="Only male or female!")


async def name(message: Message, state: FSMContext):
    if message.content_type == "text" and len(message.text) in range(3, 30):
        async with state.proxy() as data:
            data["Name"] = message.text
            await message.answer(text="Set your preference", reply_markup=PREFERENCE_MENU)
            await FSMRegister.next()
    else:
        await message.answer(text="Send me a real name")


async def preference(message: Message, state: FSMContext):
    if message.content_type == "text" and (message.text == "Male" or message.text == "Female" or message.text == "Both"):
        async with state.proxy() as data:
            data["preference"] = message.text
        await message.answer(text="Say something about you, your interests or what do you propose to do",
                             reply_markup=ReplyKeyboardRemove())
        await FSMRegister.next()
    else:
        await message.answer(text="Only male or Female!")


async def about_me(message: Message, state: FSMContext):
    if message.content_type == "text" and len(message.text) > 5:
        async with state.proxy() as data:
            data["about"] = message.text
        await message.answer("And finally, how old are you?")
        await FSMRegister.next()

    else:
        if len(message.text) <= 5:
            await message.answer(text="Tell a bit more about yourself")
        else:
            await message.answer(text="Write something about you, your interests or what do you propose to do")


async def age(message: Message, state: FSMContext):
    if message.content_type == "text" and int(message.text) in range(0, 120):
        async with state.proxy() as data:
            data["age"] = int(message.text)
        await message.answer("Form successfully created! Take a look:")
        show = tuple(data.values()) + (True,)

        await bot.send_photo(caption=F"{show[4]}, {show[7]}, {show[2]}\n{show[6]}",
                             photo=show[1],
                             reply_markup=PROFILE_MENU,
                             chat_id=message.from_user.id)

        try:
            base = DatabaseControl(_conn)
            base.delete_user(chat_id=message.from_user.id)
            base.create_user(show)
        except Exception as _ex:
            base = DatabaseControl(_conn)
            base.create_user(show)
        await state.finish()

    else:
        try:
            if int(message.text) not in range(0, 120):
                await message.answer(text="Send me a real age")
        except Exception as _ex:
            await message.answer(text="Only integers")


async def cancel(message: Message, state: FSMContext):
    if message.text == "Cancel":
        await state.finish()
        await message.answer(text="Turning you back", reply_markup=MAIN_MENU)


def form_fill_handlers():
    dp.register_message_handler(cancel, Text(equals=["Cancel"]), state=[FSMRegister.photo,
                                                                        FSMRegister.city,
                                                                        FSMRegister.gender,
                                                                        FSMRegister.name,
                                                                        FSMRegister.preference,
                                                                        FSMRegister.about,
                                                                        FSMRegister.age])
    dp.register_message_handler(initialization, Text(equals=["Refill my form 🖊", "Create new 🖊"], ignore_case=False))
    dp.register_message_handler(photo, content_types=["any"], state=FSMRegister.photo)
    dp.register_message_handler(city, content_types=["any"], state=FSMRegister.city)
    dp.register_message_handler(gender, content_types=["any"], state=FSMRegister.gender)
    dp.register_message_handler(name, content_types=["any"], state=FSMRegister.name)
    dp.register_message_handler(preference, content_types=["any"], state=FSMRegister.preference)
    dp.register_message_handler(about_me, content_types=["any"], state=FSMRegister.about)
    dp.register_message_handler(age, content_types=["any"], state=FSMRegister.age)


class Changes(StatesGroup):
    picture = State()
    about = State()
    active_true = State()


async def changes(message: Message):
    if message.text == "Change photo 📸":
        await Changes.picture.set()
        await message.answer(text="Send me your new photo", reply_markup=ReplyKeyboardRemove())

    if message.text == 'Change - "about" 📄':
        await Changes.about.set()
        await message.answer(text="Send me new 'about' paragraph", reply_markup=ReplyKeyboardRemove())

    if message.text == "I don't want to search any more 🌛":
        await Changes.active_true.set()
        await message.answer(text="are you really sure you want to disable your form?", reply_markup=DISABLE_MENU)

    if message.text == "Activate my form":
        DatabaseControl(_conn).change(column="active", data=(True,), chat_id=message.from_user.id)
        await forming(text="We remember you!", message=message, connection=_conn)


async def change_photo(message: Message, state: FSMContext):
    if message.content_type == "photo":
        DatabaseControl(_conn).change(column="photo", data=(message.photo[0].file_id,), chat_id=message.from_user.id)
        await forming(text="Picture successfully changed, Here's your form:", message=message, connection=_conn)
        await state.finish()

    else:
        await message.answer(text="Send me your new photo")


async def change_about(message: Message, state: FSMContext):
    if message.content_type == "text":
        DatabaseControl(_conn).change(column="about", data=(message.text,), chat_id=message.from_user.id)
        await forming(text="About section successfully changed, Take a look:", message=message, connection=_conn)
        await state.finish()

    else:
        await message.answer(text="Send me new 'about' paragraph")


async def disable_form(message: Message, state: FSMContext):
    if message.content_type == "text" and message.text == "Yes":
        DatabaseControl(_conn).change(column="active", data=(False,), chat_id=message.from_user.id)
        await message.answer(text="Your form is now disabled, Hope you have found someone!",
                             reply_markup=TURN_BACK_MENU)
        await state.finish()

    elif message.text == "No":
        await message.answer(text="Turning you back", reply_markup=MAIN_MENU)
        await state.finish()

    else:
        await message.answer(text="Yes/No")


def changes_handlers():
    dp.register_message_handler(changes, Text(equals=["Change photo 📸",
                                                      'Change - "about" 📄',
                                                      "I don't want to search any more 🌛",
                                                      "Activate my form"],
                                              ignore_case=False), state=None)
    dp.register_message_handler(change_photo, content_types=["any"], state=Changes.picture)
    dp.register_message_handler(change_about, content_types=["any"], state=Changes.about)
    dp.register_message_handler(disable_form, content_types=["any"], state=Changes.active_true)
