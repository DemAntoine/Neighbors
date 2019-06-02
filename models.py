from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, BooleanField
from peewee import datetime as peewee_datetime

db = SqliteDatabase('users.db')


class User(Model):
    class Meta:
        database = db
        db_table = "users"

    user_id = IntegerField()
    username = CharField(null=True)

    house = IntegerField(null=True)
    section = IntegerField(null=True)
    floor = IntegerField(null=True)
    apartment = IntegerField(null=True)

    created = DateTimeField(default=peewee_datetime.datetime.now)
    updated = DateTimeField(default=peewee_datetime.datetime.now)

    def __str__(self):
        return f'{self.user_id} - {self.username} : {self.house}-{self.section}'
