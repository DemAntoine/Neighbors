help_msg = ''' 
Щоб переглянути список сусідів:

<b>по обраному будинку</b>
Тисни:
<code>Дивитись сусідів 👫 ➡ Будинок ➡ Показати всіх в цьому будинку 🏠</code>\n
<b>по обраній секції</b>
Тисни:
<code>Дивитись сусідів 👫 ➡ Будинок ➡ Секція</code>\n
<b>по своєму будинку</b>
Тисни: <code>'Мій будинок 🏠'</code>

<b>по своїй секції</b>
Тисни: <code>'Моя секція 🔢'</code>

Щоб додати або змінити свої дані:

Тисни: <code>Змінити свої дані ✏</code>,
і вибери свої <i>будинок, секцію, поверх</i> і за бажанням вкажи <i>квартиру</i>\n
Виключні ситуації:
Якщо бажаєте додати більше однієї квартири, напишіть про це <a href="tg://user?id=422485737">Адміну</a>
'''

about_msg = '''
Це альфа версія бота, для обміну інформацією про мешканців <b>ЖК Чарівне Місто</b>
Бот працює не стабільно і постійно знаходиться в процесі розробки.
Опис функціоналу можна отримати командою /help
З пропозиціями звертайтесь до <a href="tg://user?id=422485737">Адміністратора</a>
Проект на <a href="https://github.com/DemAntoine/Neighbors">GitHub</a>
'''

house_1 = {
    'section_1': [i for i in range(1, 13)] + ['13-14'],
    'section_2': [i for i in range(1, 15)] + ['15-16'],
    'section_3': [i for i in range(1, 16)] + ['16-17'],
    'section_4': [i for i in range(1, 15)] + ['15-16'],
    'section_5': [i for i in range(1, 14)] + ['14-15'],
    'section_6': [i for i in range(1, 12)] + ['12-13'],
}

house_2 = {
    'section_1': [i for i in range(1, 14)] + ['14-15'],
    'section_2': [i for i in range(1, 15)] + ['15-16'],
    'section_3': [i for i in range(1, 16)] + ['16-17'],
    'section_4': [i for i in range(1, 15)] + ['15-16'],
    'section_5': [i for i in range(1, 13)] + ['13-14'],
    'section_6': [i for i in range(1, 12)] + ['12-13'],
}

house_3 = {
    'section_1': [i for i in range(1, 13)] + ['13-14'],
    'section_2': [i for i in range(1, 15)] + ['15-16'],
    'section_3': [i for i in range(1, 16)] + ['16-17'],
    'section_4': [i for i in range(1, 15)] + ['15-16'],
    'section_5': [i for i in range(1, 13)] + ['14-15'],
}

house_4 = {
    'section_1': [i for i in range(1, 24)] + ['24-25'],
    'section_2': [i for i in range(1, 16)] + ['16-17'],
    'section_3': [i for i in range(1, 15)] + ['15-16'],
    'section_4': [i for i in range(1, 14)] + ['14-15'],
    'section_5': [i for i in range(1, 12)] + ['12-13'],
}

houses_arr = {
    'house_1': house_1, 
    'house_2': house_2,
    'house_3': house_3, 
    'house_4': house_4
}

# for i in houses:
#     for j in i.values():
#         print(j)