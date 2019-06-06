from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, ForeignKeyField
from peewee import datetime as peewee_datetime
from models import User, Show
# from openpyxl import load_workbook

# wb_base = load_workbook(filename='workbook1.xlsx', read_only=False, keep_vba=True)
# ws_data = wb_base['sheet2']

# # ws_data.max_row

# # users = User.select()
# for i in range(29, 76):
    
#     User.create(
#         user_id = ws_data.cell(row=i, column=1).value,
#         username = ws_data.cell(row=i, column=2).value,
#         first_name = ws_data.cell(row=i, column=3).value,
#         last_name = ws_data.cell(row=i, column=4).value,
    
#         house = ws_data.cell(row=i, column=5).value,
#         section = ws_data.cell(row=i, column=6).value,
#         floor = ws_data.cell(row=i, column=7).value,
#         apartment = ws_data.cell(row=i, column=8).value,
#     )


# query = User.select().where(User.id > 10)
# query = User.delete().where(User.user_id == 138666641)
# query.execute()
# query = User.delete().where(User.user_id == 559566230)
# query.execute()

# # for i in query:
# #     print(i.id)

# # print(peewee_datetime.datetime.now())
# # print(peewee_datetime.datetime.today().day)


# # Show.create(

# #     user_id = 113471434,
# #     username = ws_data.cell(row=i, column=5).value,
# #     first_name = '',
# #     last_name = '',

# #     house = 4,
# #     section = 3,
# #     floor = 3,
# #     apartment = ws_data.cell(row=i, column=9).value,
# # )

# # Show.create(

# #     user_id = 219765776,
# # )

# User.create(

#     user_id = 138666641,
#     first_name = 'Artem',
#     last_name = 'Zhuravlov',
#     house = 3,
#     section = 3,
#     floor = 16,
#     apartment = 337,
    
# )

# User.create(

#     user_id = 559566230,
#     first_name = 'Maas',
#     # last_name = 'Zhuravlov',
#     house = 3,
#     section = 3,
#     floor = 16,
#     # apartment = 337,
    
# )


# Show.drop_table()
# Show.create_table()

string = """<b>Мешканці будинку №3</b>:

 <b>Секція 1</b>
<a href="tg://user?id=3680016">А Д</a> @DAntoine <b>2</b> <i>поверх</i> <b>400</b> <i>кв</i>
<a href="tg://user?id=524701027">Natalia Ov</a> <b>3</b> <i>поверх</i>
<a href="tg://user?id=607063192">AllusiaV </a> <b>3</b> <i>поверх</i> <b>18</b> <i>кв</i>
<a href="tg://user?id=565907125">Valexan </a> <b>5</b> <i>поверх</i>
<a href="tg://user?id=864063790">Евгений Антоничев</a> <b>5</b> <i>поверх</i>
<a href="tg://user?id=477006923">alexey toropovskii</a> <b>5</b> <i>поверх</i>
<a href="tg://user?id=704320564">Татьяна </a> <b>5</b> <i>поверх</i>
<a href="tg://user?id=749432167">Євген Український</a> <b>10</b> <i>поверх</i> <b>84</b> <i>кв</i>
<a href="tg://user?id=510073320">Влада Рог</a> <b>10</b> <i>поверх</i> <b>85</b> <i>кв</i>
<a href="tg://user?id=455465677">Natali </a> <b>10</b> <i>поверх</i> <b>87</b> <i>кв</i>
<a href="tg://user?id=365729530">Maria Tk</a> <b>10</b> <i>поверх</i>
<a href="tg://user?id=828650261">Brunetka_Kiev </a> <b>12</b> <i>поверх</i>

 <b>Секція 2</b>
<a href="tg://user?id=752256435">Nataly Volk</a> <b>2</b> <i>поверх</i>
<a href="tg://user?id=433650942">Yarik Volk</a> <b>2</b> <i>поверх</i>
<a href="tg://user?id=431757638">Andrey </a> <b>2</b> <i>поверх</i>
<a href="tg://user?id=489677484">Константин Компаниец</a> <b>3</b> <i>поверх</i>
<a href="tg://user?id=450812589">Anna Ponomarenko</a> <b>3</b> <i>поверх</i>
<a href="tg://user?id=206604359">Vlad Goloborodko</a> <b>4</b> <i>поверх</i>
<a href="tg://user?id=568932031">Oksana Zaichenko</a> <b>7</b> <i>поверх</i>
<a href="tg://user?id=200189699">Igor Dmitriv</a> <b>7</b> <i>поверх</i>
<a href="tg://user?id=477005192">Vladimir </a> <b>10</b> <i>поверх</i>
<a href="tg://user?id=641004857">Olya Kudryl</a> <b>10</b> <i>поверх</i>
<a href="tg://user?id=561985006">Олег Губарев</a> <b>12</b> <i>поверх</i>
<a href="tg://user?id=887524089">Инна Инна</a> <b>12</b> <i>поверх</i>
<a href="tg://user?id=530751630">Evhen </a> <b>13</b> <i>поверх</i>

 <b>Секція 3</b>
<a href="tg://user?id=416343237">Alexander Karpiuk</a> <b>3</b> <i>поверх</i>
<a href="tg://user?id=578046576">Elena Stepchencko</a> <b>5</b> <i>поверх</i>
<a href="tg://user?id=339798113">Ирина Панюта</a> <b>10</b> <i>поверх</i>
<a href="tg://user?id=138666641">Artem Zhuravlov</a> <b>16</b> <i>поверх</i> <b>337</b> <i>кв</i>
<a href="tg://user?id=559566230">Maas </a> <b>16</b> <i>поверх</i>

 <b>Секція 4</b>
<a href="tg://user?id=245924770">Sergey Sadovnichenko</a> <b>9</b> <i>поверх</i>
<a href="tg://user?id=391179144">DashFox </a> <b>12</b> <i>поверх</i>

 <b>Секція 5</b>
<a href="tg://user?id=206604359">Vlad Goloborodko</a> <b>1</b> <i>поверх</i>
<a href="tg://user?id=112663442">#nobody# </a> <b>3</b> <i>поверх</i>
<a href="tg://user?id=673299465">Vladimir One</a> <b>6</b> <i>поверх</i>
<a href="tg://user?id=439063206">Julia Tytarenko</a> <b>6</b> <i>поверх</i>
<a href="tg://user?id=632792685">Oleksii </a> <b>7</b> <i>поверх</i>
<a href="tg://user?id=683862590">Zoya Vasyliuk</a> <b>7</b> <i>поверх</i>
<a href="tg://user?id=404088540">Дарина </a> <b>7</b> <i>поверх</i>
<a href="tg://user?id=355228508">Svitlana Gus</a> <b>9</b> <i>поверх</i>
<a href="tg://user?id=548854570">Aleksei M</a> <b>12</b> <i>поверх</i>
<a href="tg://user?id=474740230">Сергей Василенко</a> <b>13</b> <i>поверх</i>
<a href="tg://user?id=440205513">Sergey </a> <b>14</b> <i>поверх</i>
<a href="tg://user?id=454013985">Максим </a> <b>14</b> <i>поверх</i>

 <b>Секція 6</b>

"""

# print(string)
part_1, part_2, part_3 = string.partition('<b>Секція 4')
# string.partition('<b>Секція 3</b>')[0][:-2]
# part_2 = string.rfind('<b>Секція 3</b>')
# part_3 = string[:part_2]
# part_4 = string[part_2:]
print(part_1[:-2])
print(part_2+part_3)
# print(part_4)