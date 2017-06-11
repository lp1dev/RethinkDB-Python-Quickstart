import rethinkdb as r

from thinktwice.model import Model
from thinktwice.utils import hash_salt
from thinktwice.utils import generate_jwt


class User(Model):
    def __init__(self, username, password, group=1, create=True):
        self.table = 'users'
        self.index = 'username'
        self.username = username
        if type(password) is str:
            self.password = hash_salt(password)
        else:
            self.password = password
        self.group = group
        self.one_per_index = True
        if create:
            super().__init__()

    @staticmethod
    def login(username, password):
        password_hash = hash_salt(password)
        user = User.get(username)
        if user is not None and user.password == password_hash:
            return generate_jwt(user)
        return {"error": "Connection error", "code": 401}

    @staticmethod
    def get(username):
        users = list(r.table('users').get_all(username, index="username").run())
        if len(users) is 1:
            return User._import(users[0])
        if len(users) is 0:
            return None
        return [User._import(data) for data in users]

    @staticmethod
    def _import(data):
        return User(data['username'], data['password'], data['group'], create=False)

    def export(self, export_all=False):
        if not export_all:
            return {'username': self.username,
                    'group': self.group}
        return {'username': self.username,
                'password': self.password,
                'group': self.group}
