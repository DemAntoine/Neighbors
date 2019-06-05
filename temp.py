from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, ForeignKeyField
from peewee import datetime as peewee_datetime
from models import User
# from openpyxl import load_workbook

# wb_base = load_workbook(filename='workbook1.xlsx', read_only=False, keep_vba=True)
# ws_data = wb_base['sheet2']

# ws_data.max_row

# users = User.select()
# for i in range(19, 52):
    
# User.create(

#     user_id = 848451586,
#     # username = 'demydenko',
#     first_name = 'А2',
#     # last_name = 'Демиденко',

#     house = 4,
#     section = 4,
#     floor = 4,
#     apartment = 4,
# )


# query = User.select().where(User.id > 10)
query = User.delete().where(User.user_id == 848451586)
query.execute()

# for i in query:
#     print(i.id)

# # print(peewee_datetime.datetime.now())
# # print(peewee_datetime.datetime.today().day)


# User.create(

#     user_id = 752042597,
#     # username = ws_data.cell(row=i, column=5).value,
#     first_name = 'Iryna',
#     # last_name = 'Костенко',

#     house = 2,
#     section = 1,
#     floor = 9,
#     # apartment = ws_data.cell(row=i, column=9).value,
# )
