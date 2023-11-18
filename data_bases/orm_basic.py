from datetime import datetime

import asyncpg

from environs import Env


env = Env()
env.read_env()



'''Проверка на наличие в базе'''
async def get_user(tg_id:int):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        #Данные пользователя
        user = await conn.fetchrow(f'''SELECT id_user, name_deposit, volume_stock, rating, balance 
                                        FROM users 
                                        WHERE tg_id = {tg_id}''')

        #ищем все склады и на сколько они заполнены
        stock = await conn.fetchrow(f'''SELECT SUM(stock) 
                                    FROM user_deposits 
                                    WHERE id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id})''')


        deposits = await conn.fetchrow(f'''SELECT d.name 
                                            FROM deposits d 
                                            JOIN user_deposits ud ON d.id_deposit = ud.id_deposit 
                                            WHERE ud.id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id}) 
                                            AND ud.check_status = 1''')




        return user, stock, deposits

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

'''Добавление в базу'''
async def add_user(tg_id: int, name: str):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        #Добавляем нового пользователя
        await conn.execute(f'''INSERT INTO users(tg_id, name_deposit) 
                                      VALUES($1, $2)''',
                           tg_id, name)

        #Добавляем нового рабочего
        await conn.execute(f'''INSERT INTO user_workers(id_user, id_worker, id_deposit) 
                                              VALUES((SELECT id_user FROM users WHERE tg_id = {tg_id}), 1, 1)''')

        #Добавялем стортовую шахту (Природный газ)
        await conn.execute(f'''INSERT INTO user_deposits(id_user, id_deposit, check_status) 
                                                      VALUES((SELECT id_user FROM users WHERE tg_id = {tg_id}), 1, 1)''')

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

'''Получаем все шахты пользователя'''
async def get_deposit_users(tg_id: int):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        deposits = await conn.fetch(f'''SELECT d.name, d.price, ud.
                                        FROM deposits AS d
                                        JOIN user_deposits AS ud ON d.id_deposit = ud.id_deposit
                                        WHERE ud.id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id});''')

        return deposits

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')




