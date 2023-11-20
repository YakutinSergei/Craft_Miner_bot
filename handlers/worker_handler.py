from aiogram import Router, F
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_MENU

router: Router = Router()


'''Действие по нажатию кнопки СКЛАД'''
@router.message((F.text == LEXICON_MENU['miners']))
async def miners_btn(message: Message):
    user_miner = await get_user_miner(message.from_user.id)
