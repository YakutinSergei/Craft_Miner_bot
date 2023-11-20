from aiogram import Router, F
from aiogram.types import Message

from bot_menu.menu import create_inline_kb
from data_bases.orm_basic import get_user_miner
from lexicon.lexicon_ru import LEXICON_MENU

router: Router = Router()


'''Действие по нажатию кнопки СКЛАД'''
@router.message((F.text == LEXICON_MENU['miners']))
async def miners_btn(message: Message):
    #Получаем всех рабочих и название шахты
    user_miner = await get_user_miner(message.from_user.id)

    workers = []

    for i in range(len(user_miner[0])):
        workers.append(f"{user_miner[0]['i']['name']} - {user_miner[0][i]['sum']}")

    await message.answer(text=f"Рабочие шахты: <b><i><u>{user_miner[1]['name']}</u></i></b>\n\n",
                         reply_markup= await create_inline_kb(1, f"worker_{user_miner[1]['name']}", *workers))