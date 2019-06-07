from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, ForeignKeyField
from peewee import datetime as peewee_datetime
from models import User, Show
# from openpyxl import load_workbook
#
# wb_base = load_workbook(filename='data.xlsm', read_only=False, keep_vba=True)
# ws_data = wb_base['Sheet3']

# # ws_data.max_row

# users = User.select()
# for i in range(2, 72):
#     User.create(
#         user_id=ws_data.cell(row=i, column=1).value,
#         username=ws_data.cell(row=i, column=2).value,
#         first_name=ws_data.cell(row=i, column=3).value,
#         last_name=ws_data.cell(row=i, column=4).value,
#
#         house=ws_data.cell(row=i, column=5).value,
#         section=ws_data.cell(row=i, column=6).value,
#         floor=ws_data.cell(row=i, column=7).value,
#         apartment=ws_data.cell(row=i, column=8).value,
#     )

#
# users = User.select()
# for i, user in enumerate(users, start=2):
#         ws_data.cell(row=i, column=1).value = user.user_id
#         ws_data.cell(row=i, column=2).value = user.username
#         ws_data.cell(row=i, column=3).value = user.first_name
#         ws_data.cell(row=i, column=4).value = user.last_name
#
#         ws_data.cell(row=i, column=5).value = user.house
#         ws_data.cell(row=i, column=6).value = user.section
#         ws_data.cell(row=i, column=7).value = user.floor
#         ws_data.cell(row=i, column=8).value = user.apartment
# wb_base.save(filename='data.xlsm')

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


# Show.drop_table()
# Show.create_table()

