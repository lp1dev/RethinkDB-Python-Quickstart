from hashlib import sha256
import config


def hash_salt(data):
    m = sha256()
    m.update((data + config.salt).encode(config.encoding))
    return m.digest()
