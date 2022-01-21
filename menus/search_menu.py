from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


SEARCH_MENU = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
    KeyboardButton(text="like"),
    KeyboardButton(text="dislike"),
    KeyboardButton(text="Back to main menu 🔙"),
)

ALARM_MENU = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
    KeyboardButton(text="Ok")
)

LIKE_MENU = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
    KeyboardButton(text="Who's this?")
)
