from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.keyboards import select_task


async def task_to_keyboard(all_tasks: list):
    main_kb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for i, item in enumerate(all_tasks):
        if i == 13:
            break
        buttons.append(
            InlineKeyboardButton(
                text=f'{str(item[0])} ({item[1]})',
                callback_data=select_task.new(
                    pk=str(item[2])
                ),
            )
        )
    main_kb.add(*buttons)
    return main_kb
