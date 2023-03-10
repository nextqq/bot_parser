from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import Dispatcher, FSMContext
from utils.tasks_to_buttons import task_to_keyboard
from db.functions import get_tasks_like_name
from utils.fsm import UserState
from aiogram import types

dp = Dispatcher.get_current()


@dp.message_handler(
    ChatTypeFilter(chat_type=types.chat.ChatType.PRIVATE),
    commands=['search'],
    state='*',
)
async def command_search_handler(msg: types.Message, state: FSMContext):
    text = 'Введи название задачи'
    await UserState.WaitingSearch.set()
    await msg.answer(text=text)


@dp.message_handler(
    ChatTypeFilter(chat_type=types.chat.ChatType.PRIVATE),
    content_types=types.ContentTypes.ANY,
    state=UserState.WaitingSearch,
)
async def text_search_handler(msg: types.Message, state: FSMContext):
    text = 'Выберете задачу'
    tasks = await get_tasks_like_name(
        dp['sessionmaker'],
        msg.text.strip()
    )
    main_kb = await task_to_keyboard(tasks)

    await UserState.Start.set()
    await msg.answer(
        text=text,
        reply_markup=main_kb
    )
