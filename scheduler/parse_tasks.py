from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from db.functions import delete_tasks, insert_tasks
from utils.parser import ParserTable


async def start_parse(dp: Dispatcher):

    session_maker: sessionmaker = dp['sessionmaker']
    parser = ParserTable(
        url='https://codeforces.com/problemset/page/{0}?order=BY_SOLVED_DESC',
        firs_page=1
    )
    await parser.parse_pages()
    await delete_tasks(session_maker)
    await insert_tasks(
        session_maker,
        parser.tasks_list,
        parser.types_list,
    )
