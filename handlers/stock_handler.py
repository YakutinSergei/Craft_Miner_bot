from aiogram import Router, F
from aiogram.types import Message

from data_bases.orm_basic import get_user_stock
from lexicon.lexicon_ru import LEXICON_MINES, LEXICON_PROFILE

router: Router = Router()



@router.message((F.text == LEXICON_PROFILE['warehouse']))
async def stock_btn(message: Message):
    stock_user = await get_user_stock(message.from_user.id)
    await message.answer(text='')