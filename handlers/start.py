from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import Dispatcher, FSMContext
from utils.keyboards import select_difficulty
from db.functions import get_all_difficulty
from utils.fsm import UserState
from aiogram import types

dp = Dispatcher.get_current()


@dp.message_handler(
    ChatTypeFilter(chat_type=types.chat.ChatType.PRIVATE),
    commands=['start'],
    state='*'
)
async def command_start_handler(msg: types.Message, state: FSMContext):
    text = 'Выберете сложнось\n/search - поиск по названию'
    all_difficulty = await get_all_difficulty(dp['sessionmaker'])
    main_kb = InlineKeyboardMarkup(row_width=4)
    buttons = []
    for item in all_difficulty:
        buttons.append(
            InlineKeyboardButton(
                text=str(item[0]),
                callback_data=select_difficulty.new(
                    difficulty=str(item[0])
                ),
            )
        )
    main_kb.add(*buttons)
    await UserState.Start.set()
    await msg.answer(
        text=text,
        reply_markup=main_kb
    )
