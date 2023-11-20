from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot import bot
from bot_menu.menu import create_kb_menu
from data_bases.orm_basic import add_user, get_user
#from keyboards.user_kb import create_kb_menu
from lexicon.lexicon_ru import LEXICON_PROFILE, LEXICON_MENU

router: Router = Router()

class FSMuser_add(StatesGroup):
    name = State()


@router.message(CommandStart(), F.text == LEXICON_MENU['profile'])
async def process_start_command(message: Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    #Проверяем есть ли в базе, если нет то записываем
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(text="<b><i><u>ПРОФИЛЬ</u></i></b>\n"
                                  f"<b><u>Баланс: </u></b> {user[0]['balance']}{LEXICON_PROFILE['price']}\n"
                                  f"<b><u>Заполненность склада:</u></b> {round((user[1]['sum']/user[0]['volume_stock']*100))} %\n"
                                  f"<b><u>Рейтинг:</u></b> {user[0]['rating']}", reply_markup=await create_kb_menu(user[2]['name']))
    else:
        await message.answer(text='Приветствую тебя в игре!\n'
                                  'Для начала давай придумаем название Вашего месторождения')
        await state.set_state(FSMuser_add.name)


@router.message(StateFilter(FSMuser_add.name))
async def user_name_add(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    name = message.text
    #Добавляем нового пользователя
    await add_user(tg_id, name)
    #Вызываем функцию при команде /start
    await process_start_command(message)
    await state.clear()

