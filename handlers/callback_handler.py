from db.functions import get_types_by_difficulty, get_tasks_by_types_and_difficulty, get_tasks_by_id
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.keyboards import select_difficulty, select_type, select_task
from utils.tasks_to_buttons import task_to_keyboard
from aiogram.dispatcher import Dispatcher

dp = Dispatcher.get_current()


@dp.callback_query_handler(select_difficulty.filter(), state='*')
async def callback_query_select_difficulty(call: CallbackQuery, callback_data: dict):
    difficulty = int(callback_data.get('difficulty'))
    text = 'Выберете тип'
    all_types = await get_types_by_difficulty(dp['sessionmaker'], difficulty)

    main_kb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    all_types.reverse()
    for i, item in enumerate(all_types):
        if i == 13:
            break
        buttons.append(
            InlineKeyboardButton(
                text=f'{str(item[0])} ({item[1]})',
                callback_data=select_type.new(
                    difficulty=str(difficulty),
                    type=str(item[0])[:20],
                ),
            )
        )
    main_kb.add(*buttons)
    await call.message.edit_text(
        text=text,
        reply_markup=main_kb
    )


@dp.callback_query_handler(select_type.filter(), state='*')
async def callback_query_select_type(call: CallbackQuery, callback_data: dict):
    difficulty = int(callback_data.get('difficulty'))
    task_type = str(callback_data.get('type'))
    text = 'Выберете задачу'
    all_tasks = await get_tasks_by_types_and_difficulty(
        dp['sessionmaker'],
        difficulty,
        task_type,
    )
    main_kb = await task_to_keyboard(all_tasks)

    await call.message.edit_text(
        text=text,
        reply_markup=main_kb
    )


@dp.callback_query_handler(select_task.filter(), state='*')
async def callback_query_select_task(call: CallbackQuery, callback_data: dict):
    task_id = str(callback_data.get('pk'))
    text = """
    Задача {task} ({task_id})
Темы: <i>{task_types}</i>
    Сложность: {difficulty}
    Ответили: {answer_count}
    """
    all_tasks = await get_tasks_by_id(
        dp['sessionmaker'],
        task_id,
    )
    task = all_tasks[0][1]
    difficulty = all_tasks[0][2]
    answer_count = all_tasks[0][3]
    task_types = [item[4] for item in all_tasks]

    await call.message.edit_text(
        text=text.format(
            task=task,
            task_id=task_id,
            task_types=', '.join(task_types),
            difficulty=difficulty,
            answer_count=answer_count,
        ),
        reply_markup=None
    )
