import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.keyboards import main_kb
from lexicon.lexicon import LEXICON_RU
from services import get_or_create_user


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
    await get_or_create_user(message.from_user.id, message.from_user.username) #type: ignore
    await message.answer(
        text=LEXICON_RU["/start"],
        reply_markup=main_kb
    )


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU["/help"])


@router.message(Command(commands="main"))
async def process_main_command(message: Message):
    # Заглушка получения списка задач
    tasks = [f"Задача {i} (макс 64 байта) " for i in range(5)]

    builder = InlineKeyboardBuilder()

    await message.answer(
        text="\t\t\t\t📋 Задачи etd:\t\t\t\t",
        reply_markup=builder.as_markup()
    )

    if tasks:

        for i in range(len(tasks)):
            temp_builder = InlineKeyboardBuilder()
            temp_builder.button(
                text="👁 View",
                callback_data=f"view_{i}",  # id of real task
            )

            temp_builder.button(
                text="✅ Done",
                callback_data=f"done_{i}",  # id of real task
            )

            await message.answer(
                text=f"Текст задачи {i}",  # task_title
                reply_markup=temp_builder.as_markup()
            )
        

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
