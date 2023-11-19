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
        if user:
            # Обновление склада
            await conn.execute(f'''UPDATE user_deposits
                                    SET stock = GREATEST(stock + (w.efficiency * uw.sum * EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - u.date) / 60)), 0, user.volume_stock)
                                    FROM user_workers uw
                                    JOIN workers w ON uw.id_worker = w.id_worker
                                    JOIN users u ON u.id_user = uw.id_user
                                    WHERE uw.id_deposit = user_deposits.id_deposit
                                    AND user_deposits.id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id})''')

            await conn.execute(f'''UPDATE users
                                                SET date = now()
                                                WHERE tg_id = {tg_id};''')
            

            #ищем все склады и на сколько они заполнены
            stock = await conn.fetchrow(f'''SELECT SUM(stock) 
                                        FROM user_deposits 
                                        WHERE id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id})''')


            #Имя шахты в которой сейчас
            deposits = await conn.fetchrow(f'''SELECT d.name 
                                                FROM deposits d 
                                                JOIN user_deposits ud ON d.id_deposit = ud.id_deposit 
                                                WHERE ud.id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id}) 
                                                AND ud.check_status = 1''')


            #Обновление склада
            await conn.execute(f'''UPDATE user_deposits
                                    SET stock = stock + ((w.efficiency * uw.sum) * (EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - u.date)/60)))
                                    FROM user_workers uw
                                    JOIN workers w ON uw.id_worker = w.id_worker
                                    JOIN users u ON u.id_user = uw.id_user
                                    WHERE uw.id_deposit = user_deposits.id_deposit AND user_deposits.id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id})''')


            await conn.execute(f'''UPDATE users
                                    SET date = now()
                                    WHERE tg_id = {tg_id};''')




            return user, stock, deposits

        else:
            return 0

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

        deposits = await conn.fetch(f'''SELECT d.id_deposit, d.name, d.price 
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


'''Выбор шахты'''
async def choice_deposits(id_deposit:int, tg_id:int):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        await conn.execute(f'''UPDATE user_deposits
                            SET check_status = CASE WHEN id_deposit = {id_deposit} THEN 1 ELSE 0 END
                            WHERE id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id});''')


    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')



'''Покупка шахты'''
async def bay_deposit_user(tg_id:int, deposit:str):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))


        check_dp = await conn.fetchrow(f'''SELECT d.id_deposit, d.price 
                                        FROM deposits d 
                                        JOIN user_deposits ud ON d.id_deposit = ud.id_deposit 
                                        WHERE d.name = '{deposit}'
                                        AND ud.id_user = (SELECT id_user FROM users WHERE tg_id = {tg_id});''')
        if check_dp:
            #Если такая шахта у вас уже есть
            return 0
        else:
            balance = await conn.fetchrow(f'''SELECT balance 
                                            FROM users 
                                            WHERE tg_id = {tg_id}''')
            #Узнаем цену шахты
            price_dp = await conn.fetchrow(f'''SELECT id_deposit, price 
                                                FROM deposits d 
                                                WHERE d.name = '{deposit}';''')
            if price_dp['price'] <= balance['balance']:
                #Все ок, покупаете
                # Добавялем шахту (Природный газ)
                await conn.execute(f'''INSERT INTO user_deposits(id_user, id_deposit) 
                                                                      VALUES((SELECT id_user FROM users WHERE tg_id = {tg_id}), $1)''', price_dp['id_deposit'])

                #Вычитаем баланс
                await conn.execute(f"UPDATE users "
                                   f"SET balance = balance - {price_dp['price']}"
                                   f"WHERE tg_id = {tg_id}")

                return 2


            else:
                #Не хватает денег
                return 1




    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')
