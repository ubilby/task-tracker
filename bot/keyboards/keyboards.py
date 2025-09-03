from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_builder = ReplyKeyboardBuilder()

# TODO: move texts to lexicon
button_1 = KeyboardButton(text="Настройки")
button_2 = KeyboardButton(text="Расширенный поиск")
button_3 = KeyboardButton(text="Архив")

buttons = [button_1, button_2, button_3]

kb_builder.row(*buttons, width=1)

main_kb: ReplyKeyboardMarkup = kb_builder.as_markup(
    one_time_keyboard=True, resize_keyboard=True
)
