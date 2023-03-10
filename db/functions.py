from sqlalchemy import delete, insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from db.models import Task, TaskTypes
from aiogram import Dispatcher

dp = Dispatcher.get_current()


async def delete_tasks(session_maker: sessionmaker):
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            await session.execute(delete(Task))


async def insert_tasks(session_maker: sessionmaker, tasks: list, type_tasks: list):
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            await session.execute(insert(Task), tasks)
            await session.execute(insert(TaskTypes), type_tasks)


async def get_all_difficulty(session_maker: sessionmaker):
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            result = await session.execute(
                select(
                    Task.difficulty,
                ).group_by(
                    Task.difficulty
                ).order_by(
                    Task.difficulty
                )
            )
            return result.all()


async def get_types_by_difficulty(session_maker: sessionmaker, difficulty):
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            result = await session.execute(
                select(
                    TaskTypes.name,
                    func.count(TaskTypes.id).label("count")
                ).join(
                    Task
                ).where(
                    Task.difficulty == int(difficulty)
                ).group_by(
                    TaskTypes.name
                ).order_by(
                    'count'
                )
            )
            return result.all()


async def get_tasks_by_types_and_difficulty(session_maker: sessionmaker, difficulty, task_type):
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            result = await session.execute(
                select(
                    Task.name,
                    Task.answer_count,
                    Task.id,
                ).join(
                    TaskTypes
                ).where(
                    TaskTypes.name.like(f'{task_type}%'),
                    Task.difficulty == int(difficulty),
                ).group_by(
                    Task.name,
                    Task.answer_count,
                    Task.id,
                ).order_by(
                    'answer_count'
                )
            )
            return result.all()


async def get_tasks_by_id(session_maker: sessionmaker, task_id):
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            result = await session.execute(
                select(
                    Task.id,
                    Task.name,
                    Task.difficulty,
                    Task.answer_count,
                    TaskTypes.name,
                ).join(
                    TaskTypes
                ).where(
                    Task.id == task_id
                )
            )
            return result.all()


async def get_tasks_like_name(session_maker: sessionmaker, name):
    async with session_maker() as session:
        session: AsyncSession
        async with session.begin():
            result = await session.execute(
                select(
                    Task.name,
                    Task.answer_count,
                    Task.id,
                ).join(
                    TaskTypes
                ).where(
                    Task.name.like(f'%{name}%')
                ).group_by(
                    Task.name,
                    Task.answer_count,
                    Task.id,
                ).order_by(
                    'answer_count'
                )
            )
            return result.all()
