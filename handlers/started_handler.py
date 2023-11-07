from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from data_bases.orm_basic import user_in_BD
#from keyboards.user_kb import create_kb_menu
from lexicon.lexicon_ru import LEXICON_PROFILE

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    #Проверяем есть ли в базе, если нет то записываем
    user = await user_in_BD(message.from_user.id)
    if user:
        await message.answer(text='<b><i><u>ПРОФИЛЬ</u></i></b>\n'
                                  f'<b><u>Баланс: </u></b> {user["balanc"]}{LEXICON_PROFILE["price"]}\n'
                                  f'<b><u>Заполненность склада:</u></b> {user["full_warehouse"]/user["volume_warehouse"]*100} %\n'
                                  f'<b><u>Рейтинг:</u></b> {user["rating"]}', reply_markup=create_kb_menu(user['name_deposit']))
    else:
        await message.answer(text='Приветствую тебя в игре!\n'
                                  'Для начала давай придумаем название Вашего месторождения')

