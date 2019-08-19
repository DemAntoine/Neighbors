from peewee import SqliteDatabase, IntegerField, Model, DateTimeField, CharField, ForeignKeyField, BooleanField, TextField
from datetime import datetime

db = SqliteDatabase('users.db', pragmas={'foreign_keys': 1})


def time_format():
    return datetime.now().strftime('%y.%m.%d %H:%M:%S.%f')[:-4]


class UserName(Model):
    class Meta:
        database = db
        db_table = "user_names"

    user_id = IntegerField(unique=True)
    username = CharField(null=True)
    full_name = CharField(null=True)
    created = DateTimeField(default=time_format)
    updated = DateTimeField(default=time_format, null=True)

    @property
    def href(self):
        """ inline mention of a user. works only after user write to bot first
            <a href="tg://user?id=<user_id>">inline mention of a user</a>"""
        return f'🔹<a href="tg://user?id={self.user_id}">{self.full_name}</a>'

    @property
    def username_(self):
        """if no username return empty string"""
        return '@' + self.username if self.username else ''
        
    def __str__(self):
        return f'{self.href} {self.username_}'
            

class Own(Model):
    class Meta:
        database = db
        db_table = "owns"
    
    user = ForeignKeyField(UserName, field='user_id')
    house = IntegerField(null=True)
    section = IntegerField(null=True)
    floor = IntegerField(null=True)
    apartment = IntegerField(null=True)
    created = DateTimeField(default=time_format)
    updated = DateTimeField(default=None, null=True)
    
    @property
    def floor_(self):
        """for 2-level floors. split integer from db in format 11-12"""
        return str(self.floor)[0:2] + '-' + str(self.floor)[2:4] if ((self.floor or 1) > 99) else self.floor
    
    @property
    def apartment_(self):
        """if no apartment return empty string"""
        return f'🚪 {self.apartment}' if self.apartment else ''
    
    def __str__(self):
        return f'{self.floor_ or "?"} пов. {self.apartment_}'
    
    @property
    def setting_str(self):
        return f'Буд. <b>{self.house}</b> Секц. <b>{self.section or "?"}</b> пов. <b>{self.floor_ or "?"}</b> <b>{self.apartment_}</b>'
            
    @property
    def edit_btn_str(self):
        return f'{self.house} буд. {self.section or "?"} сек. {self.floor_ or "?"} пов. {self.apartment_}'

    @property
    def joined_str(self):
        return f'{self.user} {self.setting_str}'


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
    notification_mode = CharField(null=True, default=None)

    def __str__(self):
        return f'{self.user_id} - {self.house} : {self.section}-{self.floor}'


class Jubilee(Model):
    class Meta:
        database = db
        db_table = "jubilee"

    house = IntegerField()
    count = IntegerField()
    celebrated = DateTimeField(default=time_format)


class Parking(Model):
    class Meta:
        database = db
        db_table = "parking"

    user = ForeignKeyField(UserName, field='user_id')
    parking = IntegerField(default=None, null=True)
    house = IntegerField(default=None, null=True)
    created = DateTimeField(default=time_format)

    def __str__(self):
        return f'{self.user_id} - {self.parking}'


class Chat(Model):
    class Meta:
        database = db
        db_table = "chat"
        
    user_id = IntegerField()
    full_name = CharField()
    msg_len = IntegerField()
    created = DateTimeField(default=time_format)
    msg = TextField()


if __name__ == '__main__':
    # db.drop_tables([Parking, Own], safe=True)
    db.create_tables([UserName, Own, Show, Jubilee, Parking, Chat], safe=True)
