from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.keyboards import main_kb
from lexicon.lexicon import LEXICON_RU

router = Router()
router.message.filter(F.from_user.id == 198885006)


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU["/start"],
        reply_markup=main_kb
    )


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU["/help"])


@router.message(Command(commands="main"))
async def process_main_command(message: Message):
    # Заглушка
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


def fill_task(task: str) -> str:
    if len(task) < 40:
        return task + "" * (40 - len(task))

    else:
        return task[:41]
