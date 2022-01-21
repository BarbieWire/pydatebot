from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


MAIN_MENU = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
    KeyboardButton(text="My profile 👤"),
    KeyboardButton(text="Search 🔎"),
    KeyboardButton(text="I don't want to search any more 🌛")
)

DISABLE_MENU = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
    KeyboardButton(text="Yes"),
    KeyboardButton(text="No")
)

TURN_BACK_MENU = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
    KeyboardButton(text="Activate my form")
)
