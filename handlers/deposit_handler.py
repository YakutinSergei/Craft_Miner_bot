from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot import bot
from bot_menu.menu import create_inline_kb
from data_bases.orm_basic import get_deposit_users
from lexicon.lexicon_ru import LEXICON_MINES

router: Router = Router()


@router.message(F.text == LEXICON_MINES['natural_gas']
                or F.text == LEXICON_MINES['uranium']
                or F.text == LEXICON_MINES['coal']
                or F.text == LEXICON_MINES['oil']
                or F.text == LEXICON_MINES['gold'])
async def mines(message: Message):
    await message.answer(text="⬇️Выберите шахту⬇️", reply_markup=await create_inline_kb(1, 'ch_dp', LEXICON_MINES['natural_gas'],
                                                                                                    LEXICON_MINES['uranium'],
                                                                                                    LEXICON_MINES['coal'],
                                                                                                    LEXICON_MINES['oil'],
                                                                                                    LEXICON_MINES['gold']))
@router.callback_query(F.data.startswith('ch_dp'))
async def choice_deposits(callback: CallbackQuery):
    deposit = callback.data.split('_')[-1]
    deposit_users = await get_deposit_users(callback.from_user.id)

    for i in range(len(deposit_users)):
        if deposit == deposit_users[i]['name']:
            print('Есть')