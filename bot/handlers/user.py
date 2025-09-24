import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.keyboards import main_kb
from lexicon.lexicon import LEXICON_RU
from services import display_tasks, create_task


router = Router()
# router.message.filter(F.from_user.id == 198885006)
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def process_start_command(message: Message):
    # TODO:
    # проверить, что такой пользовательсуществует
    # если нет то создать
    # предложить отправить сообщение - создать задачу
    # если есть то вывести последние 5 задач с кнопками посмотерть, добавить, выполнить
    await message.answer(
        text=LEXICON_RU["/start"],
        reply_markup=main_kb
    )

    await display_tasks(message)


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU["/help"])


@router.message(Command(commands="main"))
async def process_main_command(message: Message):
    await display_tasks(message) 
       

@router.callback_query(F.data.startswith("view_"))
async def handle_view_buttons(callback_query: CallbackQuery):
    logger.info(f"нажата кнопка view callback_query.data: {callback_query}")


@router.callback_query(F.data.startswith("done_"))
async def handle_done_buttons(callback_query: CallbackQuery):
    logger.info(f"нажата кнопка done callback_query.data: {callback_query.data}")


@router.message(F.content_type == 'text')
async def handle_text_message(message: Message):
    # создание таски
    logger.info(f"текст пойман {message}")
    await create_task(message)
