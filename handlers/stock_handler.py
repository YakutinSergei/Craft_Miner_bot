from aiogram import Router, F
from aiogram.types import Message

from data_bases.orm_basic import get_user_stock
from lexicon.lexicon_ru import LEXICON_MINES, LEXICON_PROFILE

router: Router = Router()



@router.message((F.text == LEXICON_PROFILE['warehouse']))
async def stock_btn(message: Message):
    stock_user = await get_user_stock(message.from_user.id)
    text = ''
    sum_stock = 0
    for i in range(len(stock_user)):
        text += f"{stock_user[i]['name']} - {round(stock_user[i]['stock'])}\n"
        sum_stock += round(stock_user[i]['stock'])

    print(sum_stock)
    print(stock_user[0]['volume_stock'])
    await message.answer(text=f"<b><i><u>📦СКЛАД📦</u></i></b>\n\n"
                              f"{text}\n"
                              f"Заполненность склада: {round(sum_stock/stock_user[0]['volume_stock']*100)} %")