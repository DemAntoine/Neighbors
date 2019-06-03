from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, ForeignKeyField
from peewee import datetime as peewee_datetime

db = SqliteDatabase('users.db')


class User(Model):
    class Meta:
        database = db
        db_table = "users"

    user_id = IntegerField()
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)

    house = IntegerField(null=True)
    section = IntegerField(null=True)
    floor = IntegerField(null=True)
    apartment = IntegerField(null=True)

    created = DateTimeField(default=peewee_datetime.datetime.now)
    updated = DateTimeField(default=peewee_datetime.datetime.now)

    def __str__(self):
        return f'@{self.username} -Ім\'я:{self.first_name} {self.last_name}-Будинок:{self.house}'

    def section_view(self):
        return f'@{self.username or " "} -Ім\'я:{self.first_name} {self.last_name or " "} Поверх:{self.floor or " "}'
        
    def house_view(self):
        return f'@{self.username or " "} -- Ім\'я: {self.first_name} {self.last_name or " "} -- Поверх: {self.floor}'


class Show(Model):
    class Meta:
        database = db
        db_table = "params"

    user_id = IntegerField()

    house = IntegerField(null=True)
    section = IntegerField(null=True)
    floor = IntegerField(null=True)

    def __str__(self):
        return f'{self.user_id} - {self.house} : {self.section}-{self.floor}'
