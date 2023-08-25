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
    if msg == "Старт" or msg == "Начать":
        await event.answer(message="Добро пожаловать в чат-бота! Эта инструкция поможет Вам разобраться со всеми функциями бота.\nВ самом начале Вы должны предоставить табель боту, отправив команду '.табель' и прикрепив к нему сам табель. Когда табель принят, Вы можете посмотреть список платников, которые прописаны в самом табеле. Для внесения данных об отсутствующих, Вы можете использовать команду '. (фамилия/ии)', после точки и фамилий должен быть только пробел. В конце недели Вы должны вывести табель командой 'Выведи табель', она находиться на главной странице бота. У бота также есть функция напоминалки - она оповещает Вас, если Вы не внесли данные об отсутствующих до 12 часов дня. Её можно отключить на странице настроек. Подробную информацию Вы можете получить на странице помощи.", keyboard=main_keyboard)
    elif msg == 'Список платников':
        conn = sq.connect("teachers.sqlite")
        cur = conn.cursor()
        cur.execute(f'''SELECT class_name FROM teachers_table WHERE vk_id = "{id_user}"''')
        class_name = cur.fetchone()[0]
        payers = create_list_payers(class_name)
        data = f",\n-".join(payers)
        conn.close()
        await event.answer(message=f"Список платников в Вашем классе:\n-{data}")
    elif msg == "Настройки":
        conn = sq.connect("teachers.sqlite")
        cur = conn.cursor()
        cur.execute(f'''SELECT reminder FROM teachers_table WHERE vk_id = "{id_user}"''')
        remind = cur.fetchone()[0]
        conn.close()
        await event.answer(message="Вы на странице настроек бота",
                           keyboard=(settings_keyboard_true if remind == True else settings_keyboard_false))
    elif msg == "Назад":
        await event.answer(message="Вы на главной странице бота", keyboard=main_keyboard)
    elif msg == "Напоминалка":
        conn = sq.connect("teachers.sqlite")
        cur = conn.cursor()

        cur.execute(f'''SELECT reminder FROM teachers_table WHERE vk_id = "{id_user}"''')
        remind = cur.fetchone()[0]
        if remind:
            cur.execute(f'''UPDATE teachers_table SET reminder = 0 WHERE vk_id = "{id_user}"''')
            conn.commit()
            conn.close()
            await event.answer(message=f"Напоминалка выключена", keyboard=settings_keyboard_false)
        else:
            cur.execute(f'''UPDATE teachers_table SET reminder = 1 WHERE vk_id = "{id_user}"''')
            conn.commit()
            conn.close()
            await event.answer(message=f"Напоминалка включена", keyboard=settings_keyboard_true)
    elif msg == "Помощь":
        await event.answer(message="Вы перешли на страницу помощи", keyboard=help_keyboard)
    elif msg == "Как добавить табель?":
        await event.answer(message="Для того, чтобы добавить табель, Вам необходимо отправить сообщение '.табель', и к этому же сообщению прикрепить файл с табелем, и бот Вам ответит. Если возникла проблема, можете написать репорт, как это сделать написано по кнопке 'Имеется вопрос?'")
    elif msg == "Как написать кого нет?":
        await event.answer(message="Для того, чтобы внести в табель информацию о том, кого нет, Вам необходимо написать команду '. (фамилия/ии), после точки и фамилий строго 1 пробел'")
    elif msg == "Как вывести табель?":
        await event.answer(message="Чтобы вывести табель, необходимо, чтобы сам табель (его макет) был сохранён в боте. Чтобы узнать, как это сделать, Вы можете нажать на кнопку 'Как добавить табель'. Если табель уже есть, то для того, чтобы вывести готовый табель, Вам необходимо нажать на зелёную кнопку 'Выведи табель', и табель отправиться Вам на почту, если не будет ошибок. ")
    elif msg == "Имеется вопрос?":
        await event.answer(message="Если у Вас имеется вопрос, идея или пожелание, Вы можете связаться с создателем по команде '.репорт (сообщение)'. По мере возможности, Вам ответят.")
    elif msg == "Команды":
        await event.answer(message="""Команда для заполнения табеля - '. (фамилия/ии)'. После точки и фамилий строго пробел.\nКоманда для добавления табеля - '.табель', и к этому сообщению необходимо прикрепить сам файл.""")
