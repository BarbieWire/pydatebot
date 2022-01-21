from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


PROFILE_MENU = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
    KeyboardButton(text="Refill my form 🖊"),
    KeyboardButton(text="Change photo 📸"),
    KeyboardButton(text='Change - "about" 📄'),
    KeyboardButton(text="Back to main menu 🔙")
)

GENDER_MENU = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    KeyboardButton(text="Male"),
    KeyboardButton(text="Female")
)

PREFERENCE_MENU = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
    KeyboardButton(text="Male"),
    KeyboardButton(text="Both"),
    KeyboardButton(text="Female")
)

CANCEL = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="Cancel")
)

CREATE_NEW_MENU = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="Create new 🖊"),
    KeyboardButton(text="Back to main menu 🔙")
)