from datetime import datetime
from typing import cast

from typing import List, Optional
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import create_engine, func, text

from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = 'users'
    id        : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nick_name : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    tasks     : Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    )

    @classmethod
    async def get(cls, session: AsyncSession, user_id: int):
        result = await session.execute(select(cls).where(cls.id == user_id))
        return result.scalar_one_or_none()

    @classmethod
    async def create(cls, session: AsyncSession, user_id: int, nick_name: str):
        user = cls(id=user_id, nick_name=nick_name)
        session.add(user)
        return user
    
    async def get_tasks(self, session: AsyncSession) -> list["Task"]:
        result = await session.execute(select(Task).where(Task.user_id==self.id))

        return cast(list[Task], result.scalars().all())


    # async def create_task(self, session: AsyncSession, text: str, parent_id: str) -> "Task":
    async def create_task(self, session: AsyncSession, text: str) -> "Task":
        task = Task(
            # title=text[:10],
            text=text,
            user_id=self.id
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task


class Task(Base):
    __tablename__ = "tasks"
    id        : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # сомневаюсь, что это поле нужно
    # title: Mapped[str]
    text: Mapped[str]
    # Поле, которое будет хранить id родительского элемента
    # parent_id = Column(Integer, ForeignKey('tasks.id'))    
    # Отношение к родительскому элементу
    # parent = relationship(
    #     "Task",
    #     remote_side=[id],  # указываем, что связь идет к полю id
    #     backref="children"  # обратное отношение для получения детей
    # )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(
        "User",
        back_populates="tasks"
    )