import logging
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU

def create_button(name: str) -> KeyboardButton:
    if name in LEXICON_RU:
        return KeyboardButton(text=LEXICON_RU[name])
    
    logger.error(f"LEXICON_RU doesn't contain {name}")
    return KeyboardButton(text="Временное название")


logger = logging.getLogger(__name__)

button_names = [
    "Tasks",
    "Settings",
    # "Search",
    "Archive",
]

kb_builder = ReplyKeyboardBuilder()
buttons: list[KeyboardButton] = [create_button(name) for name in button_names]
kb_builder.row(*buttons, width=1)

main_kb: ReplyKeyboardMarkup = kb_builder.as_markup(
    one_time_keyboard=True, resize_keyboard=True
)

