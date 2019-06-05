from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, ForeignKeyField
from peewee import datetime as peewee_datetime
from models import User
# from openpyxl import load_workbook

# wb_base = load_workbook(filename='workbook1.xlsx', read_only=False, keep_vba=True)
# ws_data = wb_base['sheet2']

# ws_data.max_row

# # users = User.select()
# # for i in range(19, 52):
    
# User.create(
#     user_id = ,
#     username = '',
#     first_name = '',
#     last_name = '',

#     house = 4,
#     section = 4,
#     floor = 4,
#     apartment = 4,
# )


# query = User.select().where(User.id > 10)
# query = User.delete().where(User.user_id == )
# query.execute()

# for i in query:
#     print(i.id)

# print(peewee_datetime.datetime.now())
# print(peewee_datetime.datetime.today().day)


# User.create(

#     user_id = ,
#     username = ws_data.cell(row=i, column=5).value,
#     first_name = '',
#     last_name = '',

#     house = 2,
#     section = 1,
#     floor = 9,
#     apartment = ws_data.cell(row=i, column=9).value,
# )
