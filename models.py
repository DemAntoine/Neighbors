from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, ForeignKeyField, BooleanField
from datetime import datetime

db = SqliteDatabase('users.db')


def time_format():
    return datetime.now().strftime('%y.%m.%d %H:%M:%S.%f')[:-4]


class User(Model):
    class Meta:
        database = db
        db_table = "users"

    user_id = IntegerField()
    username = CharField(null=True)
    full_name = CharField(null=True)

    house = IntegerField(null=True)
    section = IntegerField(null=True)
    floor = IntegerField(null=True)
    apartment = IntegerField(null=True)

    created = DateTimeField(default=time_format)
    updated = DateTimeField(default=None, null=True)

    def __str__(self):
        """ inline mention of a user. works only after user write to bot first
            <a href="tg://user?id=3680016">inline mention of a user</a>"""

        href = f'🔹<a href="tg://user?id={self.user_id}">{self.full_name}</a>'
        floor = str(self.floor)[0:2] + '-' + str(self.floor)[2:4] if ((self.floor or 1) > 99) else self.floor
        username = '@' + self.username if self.username else ''

        if self.apartment:
            return f'{href} {username}     {floor or "?"} пов. {self.apartment} :door:'
        else:
            return f'{href} {username}     {floor or "?"} пов.'

    def setting_str(self):
        floor = str(self.floor)[0:2] + '-' + str(self.floor)[2:4] if ((self.floor or 1) > 99) else self.floor

        return f'Будинок <b>{self.house}</b> Секція <b>{self.section or "?"}</b> поверх ' \
            f'<b>{floor or "?"}</b> кв. <b>{self.apartment or "?"}</b>'

    def edit_btn_str(self):
        floor = str(self.floor)[0:2] + '-' + str(self.floor)[2:4] if ((self.floor or 1) > 99) else self.floor

        return f'Будинок {self.house} Секція {self.section or "?"} пов. {floor or "?"} кв. {self.apartment or "?"}'

    def user_created(self):
        floor = str(self.floor)[0:2] + '-' + str(self.floor)[2:4] if ((self.floor or 1) > 99) else self.floor
        href = f'🔹<a href="tg://user?id={self.user_id}">{self.full_name}</a>'
        username = '@' + self.username if self.username else ''
        if self.apartment:
            return f'{href} {username} дом {self.house} сек. {self.section or "?"} эт. {floor or "?"} кв. {self.apartment} id {self.user_id}'
        else:
            return f'{href} {username} дом {self.house} сек. {self.section or "?"} эт. {floor or "?"} id {self.user_id}'


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
