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
        # inline mention of a user. seems like works only after user write to bot first
        # <a href="tg://user?id=3680016">inline mention of a user</a>
        href = f'<a href="tg://user?id={self.user_id}">{self.first_name} {self.last_name or ""}</a>'
        if self.username:
            return f'{href} @{self.username} {self.floor} поверх'
        else:
            return f'{href} {self.floor} поверх'

    # def section_view(self):
    #     href = f'<a href="tg://user?id={self.user_id}">{self.first_name} {self.last_name or ""}</a>'
    #     if self.username:
    #         return f'{href} @{self.username} {self.floor} поверх'
    #     else:
    #         return f'{href} {self.floor} поверх'
    #
    # def house_view(self):
    #     href = f'<a href="tg://user?id={self.user_id}">{self.first_name} {self.last_name or ""}</a>'
    #     if self.username:
    #         return f'{href} @{self.username} {self.floor} поверх'
    #     else:
    #         return f'{href} {self.floor} поверх'


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
