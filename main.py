from loader import dp
from aiogram import executor
from admin_notice import shutdown, startup
from profile.formfill import form_fill_handlers, changes_handlers
from commands.commands import commands_file_handlers
from messages.main_menu_response import main_menu_response_handler


form_fill_handlers()
changes_handlers()
commands_file_handlers()
main_menu_response_handler()


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=startup, on_shutdown=shutdown)
