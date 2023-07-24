from vkbottle.bot import BotLabeler, Message
from .keyboards import *
from .utils import *
import sqlite3 as sq

bl = BotLabeler()


@bl.private_message(text='@id')
async def id_claimer(event: Message):
    id_person = await event.get_user(id)
    await event.answer(message=id_person)


@bl.private_message()
async def main_handler(event: Message):
    msg = event.text
    id_user = f"id{(await event.get_user(id)).get('id')}"
    if msg == 'старт' or msg == 'начать':
        await event.answer(message='Бот запущен, вы на главной странице', keyboard=main_keyboard)
    elif msg == 'Список платников':
        conn = sq.connect("teachers.sqlite")
        cur = conn.cursor()
        cur.execute(f'''SELECT class_name FROM teachers_table WHERE vk_id = "{id_user}"''')
        class_name = cur.fetchone()[0]
        payers = create_list_payers(class_name)
        data = f',\n-'.join(payers)
        conn.close()
        await event.answer(message=f'Список платников в Вашем классе:\n-{data}')
    elif msg == 'Настройки':
        conn = sq.connect("teachers.sqlite")
        cur = conn.cursor()
        cur.execute(f'''SELECT reminder FROM teachers_table WHERE vk_id = "{id_user}"''')
        remind = cur.fetchone()[0]
        conn.close()
        await event.answer(message='Вы на странице настроек бота',
                           keyboard=(settings_keyboard_true if remind == True else settings_keyboard_false))
    elif msg == 'Назад':
        await event.answer(message='Вы на главной странице бота', keyboard=main_keyboard)
    elif msg == 'Напоминалка':
        conn = sq.connect("teachers.sqlite")
        cur = conn.cursor()

        cur.execute(f'''SELECT reminder FROM teachers_table WHERE vk_id = "{id_user}"''')
        remind = cur.fetchone()[0]
        if remind:
            cur.execute(f'''UPDATE teachers_table SET reminder = 0 WHERE vk_id = "{id_user}"''')
            conn.commit()
            conn.close()
            await event.answer(message=f'Напоминалка выключена', keyboard=settings_keyboard_false)
        else:
            cur.execute(f'''UPDATE teachers_table SET reminder = 1 WHERE vk_id = "{id_user}"''')
            conn.commit()
            conn.close()
            await event.answer(message=f'Напоминалка включена', keyboard=settings_keyboard_true)
    elif msg == 'Помощь':
        await event.answer()
