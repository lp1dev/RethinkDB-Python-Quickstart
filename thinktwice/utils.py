from hashlib import sha256
import jwt
import config


def generate_jwt(user):
    return {'token': jwt.encode(user.export(), config.secret, algorithm='HS256')}


def hash_salt(data):
    m = sha256()
    m.update((data + config.salt).encode(config.encoding))
    return m.digest()
