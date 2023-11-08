LEXICON_RU: dict[str, str] = {
    '/start': 'Введите Ваше имя\n'
              '<i>Имя должно быть уникальным</i>',
    '/help': 'Это очень простая игра. Мы одновременно должны '
             'сделать выбор одного из трех предметов. Камень, '
             'ножницы или бумага.\n\nЕсли наш выбор '
             'совпадает - ничья, а в остальных случаях камень '
             'побеждает ножницы, ножницы побеждают бумагу, '
             'а бумага побеждает камень.\n\n<b>Играем?</b>',
    'order': 'Заказать!',
    'other_answer': 'Извини, увы, это сообщение мне непонятно...',
    'login_true':'Такой логин уже существует\n'
                 'Попробуйте еще раз',
    'login_false':'Добро пожаловать, ',
    'login_user_true': 'Добро пожаловать, ',
    'login_user_false': 'Вы указали не верный логин',
    'back': 'НАЗАД',
    'universe': 'Выбрать вселенную',
    'add_card': 'Получить карту',
    'my_cards': 'Мои карты'}


# Меню
LEXICON_MENU: dict[str, str] = {
    'miners' : '⛏️Шахтеры',
    'warehouse' : '📦Склад',
    'market' : '🏦Рынок',
    'profile' : '⚙️Профиль',
    'shop' : '💰Магазин',
}


#Шахты
LEXICON_MINES: dict[str, str] = {
    'natural_gas' : '⛽️Природный газ✅',
    'uranium' : '☢️Уран❌',
    'coal' : '🪨Уголь❌',
    'oil' : '🛢Нефть❌',
    'gold' : '🟡Золото❌',
    'uranium_open' : '☢️Уран✅',
    'coal_open' : '🪨Уголь✅',
    'oil_open' : '🛢Нефть✅',
    'gold_open' : '🟡Золото✅'
}

# Профиль
LEXICON_PROFILE: dict[str, str] = {
    'profile' : '👷🏼‍♂️Профиль',
    'balance' : '🏦Баланс',
    'warehouse' : '📦Склад',
    'rating' : '🥇Рейтинг',
    'price': '💵',
    'extraction':'⚒Добыча полезных ископаемых'
}