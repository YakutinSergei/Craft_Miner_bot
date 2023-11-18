from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot import bot
from bot_menu.menu import create_kb_menu
from data_bases.orm_basic import add_user, get_user
#from keyboards.user_kb import create_kb_menu
from lexicon.lexicon_ru import LEXICON_PROFILE, LEXICON_MINES

router: Router = Router()


@router.message(F.text == LEXICON_MINES['natural_gas']
                or F.text == LEXICON_MINES['uranium']
                or F.text == LEXICON_MINES['coal']
                or F.text == LEXICON_MINES['oil']
                or F.text == LEXICON_MINES['gold'])
async def mines(message: Message):
    await message.answer(text="Выберите шахту", reply_markup=await create_kb_menu('ПУСТО'))
