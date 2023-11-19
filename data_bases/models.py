from datetime import datetime, timedelta

import asyncpg

from environs import Env

env = Env()
env.read_env()


async def db_connect():
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))


        #Таблица юзеры
        #id_user - порядковый номер пользователя
        #tg_id - ID пользователя в телеграм
        #name_deposit - Имя месторождения
        #volume_stock - Размер склада
        #rating - рейтинг игрока
        #balance - баланс
        await conn.execute('''CREATE TABLE IF NOT EXISTS users(id_user SERIAL NOT NULL PRIMARY KEY, 
                                                                tg_id BIGSERIAL, 
                                                                name_deposit TEXT NOT NULL,
                                                                volume_stock INTEGER DEFAULT '100',
                                                                rating INTEGER DEFAULT '0',
                                                                date TIMESTAMP DEFAULT 'now()'
                                                                balance INTEGER DEFAULT '0')''')

        #МЕСТОРОЖДЕНИЯ
        #id_deposit - порядкойвый номер месторождения
        #name - имя месторождения
        #price - цена месторождения
        await conn.execute('''CREATE TABLE IF NOT EXISTS deposits(id_deposit SERIAL NOT NULL PRIMARY KEY, 
                                                                    name TEXT NOT NULL,
                                                                    price INTEGER NOT NULL)''')

        #РАБОЧИЕ
        #id_worker - порядковый номер рабочего
        #name - имя рабочего
        #price - цена первоначальная
        #efficiency - производительность в час
        await conn.execute('''CREATE TABLE IF NOT EXISTS workers(id_worker SERIAL NOT NULL PRIMARY KEY, 
                                                                name TEXT NOT NULL,
                                                                price INTEGER NOT NULL,
                                                                efficiency INTEGER NOT NULL);''')

        #РАБОЧИЕ ПОЛЬЗОВАТЕЛЯ
        #id_user - порядковый номер пользователя
        #id_worker - порядковый номер
        #id_deposit - порядковый номер месторождения
        #lvl- уровень рабочего
        # sum - количество рабочих
        await conn.execute('''CREATE TABLE IF NOT EXISTS user_workers(id_user INTEGER REFERENCES users(id_user) NOT NULL, 
                                                                        id_worker INTEGER REFERENCES workers(id_worker) NOT NULL,
                                                                        id_deposit INTEGER REFERENCES deposits(id_deposit) NOT NULL,
                                                                        lvl INTEGER DEFAULT '1',
                                                                        sum INTEGER DEFAULT '1');''')

        #МЕТОРОЖДЕНИЯ ПОЛЬЗОВАТЕЛЯ
        #id_user - порядковый номер пользователя
        #id_deposit - порядковый номер месторождения
        #stok - склад
        #check - выбран склад
        await conn.execute('''CREATE TABLE IF NOT EXISTS user_deposits(id_user INTEGER REFERENCES users(id_user) NOT NULL, 
                                                                        id_deposit INTEGER REFERENCES deposits(id_deposit) NOT NULL,
                                                                        stock INTEGER DEFAULT '0',
                                                                        check_status INTEGER DEFAULT '0')''')




    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
          if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')