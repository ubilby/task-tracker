import logging
from db import async_session
from models import User, Task
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


logger = logging.getLogger(__name__)

async def get_or_create_user(message: Message) -> User:
    user_id: int = message.from_user.id # type: ignore
    nick_name: str = message.from_user.username # type: ignore
    async with async_session() as session:  # type: ignore
        user = await User.get(session, user_id)
        if not user:
            user = await User.create(session, user_id, nick_name)
            await session.commit()
            await session.refresh(user)
            logger.info(f"Создан новый пользователь {user_id}")
        return user


async def get_tasks(user: User, message: Message) -> list[Task]:
    tasks = []
    
    async with async_session() as session:  # type: ignore
        if user:
            tasks = await user.get_tasks(session)

    return tasks


async def display_tasks(message: Message):
    user = await get_or_create_user(message)
    tasks = await get_tasks(user, message)

    for task in tasks:  # ignore: type
        temp_builder = InlineKeyboardBuilder()
        temp_builder.button(
            text="👁 View",
            callback_data=f"view_{task.id}",  # id of real task
        )

        temp_builder.button(
            text="✅ Done",
            callback_data=f"done_{task.id}",  # id of real task
        )

        await message.answer(
            text=f"{task.text}",  # task_title
            reply_markup=temp_builder.as_markup()
        )


async def create_task(message: Message):
    user = await get_or_create_user(message)
    
    # <<!! подумать)
    if not message.text:
        return
    
    async with async_session() as session:  # type: ignore
            tasks = await user.create_task(session, message.text)
