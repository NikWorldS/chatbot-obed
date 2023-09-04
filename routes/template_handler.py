from vkbottle.bot import BotLabeler, Message
import requests
from .utils import create_template, create_list_payers, generate, filling_template
from .db_connector import execute_query, execute_update
from dotenv import load_dotenv, find_dotenv
from os import getenv
import datetime

load_dotenv(find_dotenv())
admin_id = int(getenv('ADMIN_ID'))

bl = BotLabeler()


@bl.private_message(text=['/табель', ".табель"])
async def create_layout(event: Message):
    attach = event.attachments

    if attach.__len__() > 0:
        document = attach[0].doc

        if document is None:
            return

        name, type_f = document.title.split(".")
        if type_f == 'xlsx':
            response = requests.get(document.url)
            with open(document.title, "wb") as f:
                f.write(response.content)
            create_temp = create_template(f"{document.title}")
            await event.answer(create_temp)
        elif type_f != 'xlsx':
            await event.answer(
                f'Возможно, отправленный файл не является табелем.\nЕсли ошибка повторяется, напишите @id{admin_id}')
    elif attach.__len__() == 0:
        await event.answer(f'К сообщению не прикреплён файл, прикрепи его, и напиши ту же команду в ОДНОМ сообщении')


@bl.private_message(text='. <missing>')
async def filling_tabel(event: Message, missing):
    if datetime.datetime.today().weekday() == 6:
        await event.answer(message="Сегодня воскресенье, ничего записываться не будет")
        return
    payers_dict = {}

    id_user = f"id{(await event.get_user(id)).get('id')}"


    class_name = (execute_query(f"""SELECT class_name FROM teachers_table WHERE teacher_vk_id = '{id_user}'""")[0][0])


    missing = missing.split()

    payers = create_list_payers(class_name)
    for payer in payers:
        payers_dict[payer] = 'н'

    for person in payers_dict:
        if person in missing:
            payers_dict[person] = 'н'
        else:
            payers_dict[person] = 1

    execute_update(f"""UPDATE teachers_table SET next_answer_time = {generate()} WHERE teacher_vk_id = '{id_user}'""")
    values_list = list(payers_dict.values())
    filling_template(values_list, class_name)
    await event.answer(f"Сегодня {len(values_list) - values_list.count('н')} из {len(values_list)} платников")
