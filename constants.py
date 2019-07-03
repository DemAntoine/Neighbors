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

building_msg = '''
🏗<b>Хід будівництва ЖК</b>🏗

<b>Корисні посилання</b>
🔸 <a href="https://jk-charivnemisto.com.ua/">Сайт ЖК (УкрБуд)</a>
🔸 <a href="https://z-capital.com.ua/">Сайт ФК "Житло капитал"</a>
🔸 <a href="https://gdevkievezhithorosho.com/2016/08/чарівне-місто-укрбуд/">Обзор ЖК на сайте "ГдевКиевежитьхорошо"</a>
🔸 <a href="https://kotsiuba.com/project/terytoria-zhk-charivne-misto">Концепція влаштування території ЖК Чарівне місто"</a>

<b>Відділ продажів</b>
🔹 Біля ЖК: (м. Червоний хутір) - (044) 364 49 28
🔹 Головний офіс: вул. Сверстюка, 23, 1-й поверх - (044) 390 30 86

<b>Демонстраційний поверх</b>
<i>(1 дім, 1 секція, 3 поверх)</i>
Запис на відвідування тільки на місці у менеджерів
    Будні: 11:00-13:00
                15:00-17:00
    Субота: 10:00-12:00
    Неділя: SORRY

<b>Онлайн камери</b>
🔹 <a href="http://vs8.videoprobki.com.ua/tvukrbud/cam3.mp4">№1 - вид зверху на 1-2 дім</a>
🔹 <a href="http://vs8.videoprobki.com.ua/tvukrbud/cam28.mp4">№2 - двір 1 дому</a>
🔹 <a href="http://vs9.videoprobki.com.ua/tvukrbud/cam44.mp4">№3 - 3 дім</a>
🔹 <a href="https://www.youtube.com/playlist?list=PLrQXA1HhBGJLmMltX0P-qLNZp1Vg6FpX-">Прогрес будівництва за місяць</a>
<i>відеоколаж з камери від</i> @silent_twilight

<b>Динаміка будівництва (фото)</b>
🔹 <a href="https://jk-charivnemisto.com.ua/ru/building">Архів на офіційному сайті</a>
🔹 <a href="https://novostroyki.lun.ua/жк-чаривне-мисто-киев/ход-строительства">Архів на Лун.ua</a>

<b>Відео з дрона</b>
🔹 <a href="">Много облетов от Ильи Воронкова</a>
🔹 <a href="">от 10 июня 2017</a>
🔹 <a href="">от 28 апреля 2018</a>
🔹 <a href="">Аэрооблет май 2018</a>
🔹 <a href="">Аэрооблет 31 марта 2019</a>

<b>Ми на карті</b>
🔹 2гис
🔹 google.com

🔹 Когда светит солнце в мое окно? Посмотреть можно тут - suncalc<b></b>

<b>Суди</b>
Открываем @OpenDataUABot, вводим номер дела 910/3435/17,826/16071/18 и получаем всю актуальную информацию по заседаниям, решениям и т.д.
'''

house_1 = {
    'section_1': [i for i in range(1, 15)] + ['12-13', '13-14'],
    'section_2': [i for i in range(1, 17)] + ['14-15', '15-16'],
    'section_3': [i for i in range(1, 16)] + ['16-17'],
    'section_4': [i for i in range(1, 15)] + ['15-16'],
    'section_5': [i for i in range(1, 16)] + ['13-14', '14-15'],
    'section_6': [i for i in range(1, 14)] + ['11-12', '12-13'],
}

house_2 = {
    'section_1': [i for i in range(1, 16)] + ['12-13', '13-14', '14-15'],
    'section_2': [i for i in range(1, 17)] + ['14-15', '15-16'],
    'section_3': [i for i in range(1, 16)] + ['16-17'],
    'section_4': [i for i in range(1, 15)] + ['15-16'],
    'section_5': [i for i in range(1, 13)] + ['13-14'],
    'section_6': [i for i in range(1, 14)] + ['11-12', '12-13'],
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
    'house_4': house_4,
}
