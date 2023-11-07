from datetime import datetime

import asyncpg

from environs import Env


env = Env()
env.read_env()



'''Проверка на наличие в базе'''
async def user_in_BD(tg_id):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))


        user = await conn.fetchrow(f'''SELECT id_user FROM users WHERE tg_id = {tg_id}''')
        return user

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')