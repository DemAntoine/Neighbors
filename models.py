from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, ForeignKeyField, BooleanField
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
        """ inline mention of a user. seems like works only after user write to bot first
            <a href="tg://user?id=3680016">inline mention of a user</a>"""
            
        href = f'<a href="tg://user?id={self.user_id}">{self.first_name} {self.last_name or ""}</a>'
        if self.username:
            if self.apartment:
                return f'{href} @{self.username}     {self.floor or "?"} ⏫ {self.apartment} 🚪'
            else:
                return f'{href} @{self.username}     {self.floor or "?"} ⏫'
        else:
            if self.apartment:
                return f'{href}    {self.floor or "?"} ⏫ {self.apartment} 🚪'
            else:
                return f'{href}    {self.floor or "?"} ⏫'

    def setting_str(self):
        return f'Будинок <b>{self.house}</b> Секція <b>{self.section or "?"}</b> поверх ' \
            f'<b>{self.floor or "?"}</b> кв. <b>{self.apartment or "?"}</b>'

    def edit_btn_str(self):
        return f'Будинок {self.house} Секція {self.section or "?"} поверх {self.floor or "?"} кв. {self.apartment or "?"}'


class Show(Model):
    class Meta:
        database = db
        db_table = "params"

    user_id = IntegerField()

    house = IntegerField(null=True)
    section = IntegerField(null=True)
    floor = IntegerField(null=True)

    owns = IntegerField(null=True)
    
    msg_apart_mode = BooleanField(null=True, default=False)

    def __str__(self):
        return f'{self.user_id} - {self.house} : {self.section}-{self.floor}'
