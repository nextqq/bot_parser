from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    Start = State()
    WaitingSearch = State()
