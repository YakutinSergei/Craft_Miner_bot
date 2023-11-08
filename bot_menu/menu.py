from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_MENU


async def create_kb_menu(mines):
    btn_mines: KeyboardButton = KeyboardButton(text=mines)
    btn_miners: KeyboardButton = KeyboardButton(text=LEXICON_MENU['miners'])
    btn_warehouse: KeyboardButton = KeyboardButton(text=LEXICON_MENU['warehouse'])
    btn_market: KeyboardButton = KeyboardButton(text=LEXICON_MENU['market'])
    btn_profile: KeyboardButton = KeyboardButton(text=LEXICON_MENU['profile'])
    btn_shop: KeyboardButton = KeyboardButton(text=LEXICON_MENU['shop'])
    menu_user: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_mines, btn_miners],
                                                                            [btn_warehouse, btn_market], [btn_profile, btn_shop]],
                                                                    resize_keyboard=True)
    return menu_user