from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot import bot
from bot_menu.menu import create_inline_kb, create_kb_menu
from data_bases.orm_basic import get_deposit_users, choice_deposits, get_user, bay_deposit_user
from lexicon.lexicon_ru import LEXICON_MINES, LEXICON_MENU

router: Router = Router()


@router.message(F.text == [LEXICON_MINES['natural_gas'],
                           LEXICON_MINES['uranium'],
                           LEXICON_MINES['coal'],
                           LEXICON_MINES['oil'],
                           LEXICON_MINES['gold']])
async def mines(message: Message):
    await message.answer(text="⬇️Выберите шахту⬇️", reply_markup=await create_inline_kb(1, 'ch_dp_', LEXICON_MINES['natural_gas'],
                                                                                                    LEXICON_MINES['uranium'],
                                                                                                    LEXICON_MINES['coal'],
                                                                                                    LEXICON_MINES['oil'],
                                                                                                    LEXICON_MINES['gold']))

'''выбор шахты'''
@router.callback_query(F.data.startswith('ch_dp'))
async def process_choice_deposits(callback: CallbackQuery):
    #Получаем имя нашей шахты
    deposit = callback.data.split('_')[-1]
    #Получаем все имена наших шахт
    deposit_users = await get_deposit_users(callback.from_user.id)
    #Ставить флажок на наличие шахты
    check_dep = 0
    #Проверяем есть ли такая шахты у нас
    for i in range(len(deposit_users)):
        if deposit == deposit_users[i]['name']:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await callback.message.answer(text=f"Вы перешли в шахту: {deposit}",
                                          reply_markup=await create_kb_menu(deposit))
            #Выбраной шахте ставит 1 остальным 0
            await choice_deposits(deposit_users[i]['id_deposit'], callback.from_user.id)

            #Если такая шахты есть, ставим флаг на 1 и выходим из цикла
            check_dep = 1
            break

    #Проверяем если у нас такой шахты нет
    if not check_dep:
        await callback.message.edit_text(text=f"Шахта: {deposit} Вам пока недоступна\n"
                                              f"Для того что бы открыть нажмите кнопку ниже",
                                         reply_markup=await create_inline_kb(1, f'bay_dp_{deposit}_', LEXICON_MINES['bay_deposits'],
                                                                                                    LEXICON_MENU['back']))


'''Покупка шахты'''
@router.callback_query(F.data.startswith('bay_dp_'))
async def process_bay_deposits(callback: CallbackQuery):
    if callback.data.split('_')[-1] == LEXICON_MENU['back']:
        await callback.message.edit_text(text="⬇️Выберите шахту⬇️", reply_markup=await create_inline_kb(1, 'ch_dp_', LEXICON_MINES['natural_gas'],
                                                                                                    LEXICON_MINES['uranium'],
                                                                                                    LEXICON_MINES['coal'],
                                                                                                    LEXICON_MINES['oil'],
                                                                                                    LEXICON_MINES['gold']))
    else:
        tg_id = callback.from_user.id
        deposits = callback.data.split('_')[2]
        bay_dp_user = await bay_deposit_user(tg_id, deposits)
        if bay_dp_user == 0:
            await callback.message.answer(text="Эта шахта у вас уже есть", show_alert=True)
        elif bay_dp_user == 1:
            await callback.message.answer(text="Недостаточно средств", show_alert=True)
        else:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await callback.message.answer(text="Поздравляю с покупкой", show_alert=True)

    await callback.answer()

