from vkbottle.bot import BotLabeler, Message
from vkbottle import GroupEventType, GroupTypes
from .utils import *
from .keyboards import *
import sqlite3 as sq

admin_id = 323048042

bl = BotLabeler()


@bl.private_message(text='Выведи табель')
async def tabel_sender(event: Message):
    await event.answer('Вы подтверждаете отправку табеля?', keyboard=confirm_keyboard)


@bl.private_message(text=['@add_teacher <add_teach_args>', '@добавить учителя <add_teach_args>'])
async def add_teacher(event: Message, add_teach_args):
    if (await event.get_user(id)).get('id') == admin_id:
        if add_teach_args == "help":
            await event.answer(message="ФИО | Класс | idVK-ID | Почта")
        else:
            global add_teacher_name, add_class_name, add_vk_id, add_email
            add_teacher_name, add_class_name, add_vk_id, add_email = add_teach_args.split(', ')
            await event.answer(
                message=f'Вы хотите добавить учителя @{add_vk_id}({add_teacher_name})\n {add_class_name} класса (почта: {add_email}) '
                        f'класса. Если все данные верны, подтвердите',
                keyboard=confirm_keyboard_2)


@bl.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def confirm_handler(event: GroupTypes.MessageEvent):
    cmd_send = event.object.payload['cmd_send']
    cmd_add = event.object.payload['cmd_add']

    user_id = event.object.user_id

    if cmd_send == 'agree_send':
        conn = sq.connect("teachers.sqlite")
        cur = conn.cursor()

        (cur.execute(f'''SELECT class_name, teacher_email FROM `teachers_table` WHERE vk_id == "id{user_id}"'''))
        class_n, email = cur.fetchone()
        conn.close()

        send_tab = send_tabel(class_name=class_n, mail=email)
        await event.ctx_api.messages.edit(peer_id=user_id, conversation_message_id=event.object.conversation_message_id,
                                          message=send_tab)
    elif cmd_send == 'disagree_send':
        await event.ctx_api.messages.edit(peer_id=user_id, conversation_message_id=event.object.conversation_message_id,
                                          message='Табель не отправлен')

    if cmd_add == 'agree_add':
        conn = sq.connect("teachers.sqlite")
        cur = conn.cursor()
        cur.execute(
            f'''INSERT OR IGNORE INTO teachers_table(teacher_name, vk_id, class_name, teacher_email, reminder) VALUES("
                {add_teacher_name}", "{add_vk_id}", "{add_class_name}", "{add_email}", 0)''')
        conn.commit()
        conn.close()
        await event.ctx_api.messages.edit(peer_id=user_id, conversation_message_id=event.object.conversation_message_id,
                                          message='Учитель добавлен в базу данных')
    elif cmd_add == 'disagree_add':
        await event.ctx_api.messages.edit(peer_id=user_id, conversation_message_id=event.object.conversation_message_id,
                                          message='Учитель не добавлен в базу данных')
