from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot_menu.menu import create_inline_kb
from data_bases.orm_basic import get_user_stock, up_stock_user
from lexicon.lexicon_ru import LEXICON_MENU

router: Router = Router()


'''Действие по нажатию кнопки СКЛАД'''
@router.message((F.text == LEXICON_MENU['warehouse']))
async def stock_btn(message: Message):
    #Получаем все шахты пользователя
    stock_user = await get_user_stock(message.from_user.id)
    text = ''
    sum_stock = 0
    #Формурием текст для вывода
    for i in range(len(stock_user)):
        text += f"{stock_user[i]['name']} - {round(stock_user[i]['stock'])}\n"
        sum_stock += round(stock_user[i]['stock'])
    #Выводим сообщение
    await message.answer(text=f"<b><i><u>📦СКЛАД📦</u></i></b>\n\n"
                              f"{text}\n"
                              f"Заполненность склада: {round(sum_stock/stock_user[0]['volume_stock']*100)} %",
                         reply_markup=await create_inline_kb(1, 'stock_up_', LEXICON_MENU['stock_up']))

'''Улучшение склада'''
@router.callback_query(F.data.startswith('stock_up_'))
async def process_stock_up_user(callback: CallbackQuery):
    #улучшение склада
    check_stock = await up_stock_user(callback.from_user.id)
    #Проверяем получилось ли улучшить
    if check_stock:
        # Получаем все шахты пользователя
        stock_user = await get_user_stock(callback.from_user.id)
        text = ''
        sum_stock = 0
        # Формурием текст для вывода
        for i in range(len(stock_user)):
            text += f"{stock_user[i]['name']} - {round(stock_user[i]['stock'])}\n"
            sum_stock += round(stock_user[i]['stock'])
        # Выводим сообщение
        await callback.message.edit_text(text=f"<b><i><u>📦СКЛАД📦</u></i></b>\n\n"
                                  f"{text}\n"
                                  f"Заполненность склада: {round(sum_stock / stock_user[0]['volume_stock'] * 100)} %",
                             reply_markup=await create_inline_kb(1, 'stock_up_', LEXICON_MENU['stock_up']))
        await callback.answer(text='✅Склад улучшен', show_alert=True)
        
    else:
        await callback.answer(text='❌Недостаточно средств', show_alert=True)


