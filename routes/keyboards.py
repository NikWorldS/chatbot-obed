from vkbottle import Keyboard, KeyboardButtonColor, Callback, Text


confirm_keyboard = {
    Keyboard(inline=True)
    .add(Callback('✅Да', {'cmd_send': 'agree_send', 'cmd_add': 'a'}), KeyboardButtonColor.POSITIVE)
    .add(Callback('❌Нет', {'cmd_send': 'disagree_send', 'cmd_add': 'd'}), KeyboardButtonColor.NEGATIVE)
}

confirm_keyboard_2 = {
    Keyboard(inline=True)
    .add(Callback('✅Да', {'cmd_send': 'a', 'cmd_add': 'agree_add'}), KeyboardButtonColor.POSITIVE)
    .add(Callback('❌Нет', {'cmd_send': 'd', 'cmd_add': 'disagree_add'}), KeyboardButtonColor.NEGATIVE)
}

main_keyboard = {
    Keyboard()
    .add(Text('Выведи табель'), KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Помощь"), KeyboardButtonColor.PRIMARY)
    .add(Text('Список платников'))
    .row()
    .add(Text('Настройки'))
}

settings_keyboard_true = {
    Keyboard()
    .add(Text('Напоминалка'), KeyboardButtonColor.POSITIVE)
    .add(Text('Назад'), KeyboardButtonColor.NEGATIVE)
}

settings_keyboard_false = {
    Keyboard()
    .add(Text('Напоминалка'), KeyboardButtonColor.NEGATIVE)
    .add(Text('Назад'), KeyboardButtonColor.NEGATIVE)
}

help_keyboard = {
    Keyboard()
    .add(Text("Как добавить табель?"), KeyboardButtonColor.PRIMARY)
    .add(Text("Как написать кого нет?"),KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Как вывести табель?"), KeyboardButtonColor.PRIMARY)
    .add(Text("Имеется вопрос?"),KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Назад"), KeyboardButtonColor.NEGATIVE)
}
