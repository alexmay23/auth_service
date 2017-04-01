import datetime
from passlib.context import CryptContext


def date_or_now(value):
    return value if value else datetime.datetime.utcnow()


def password_hash(value):
    pwd_context = CryptContext(
        schemes="pbkdf2_sha256",
        all__vary_rounds=0.1,
        pbkdf2_sha256__default_rounds=8000,
    )
    return pwd_context.encrypt(value.encode('utf-8'))


def validate_password_hash(password, pwd_hash):
    pwd_context = CryptContext(
        schemes="pbkdf2_sha256",
        all__vary_rounds=0.1,
        pbkdf2_sha256__default_rounds=8000,
    )
    try:
        return pwd_context.verify(password, pwd_hash)
    except ValueError:
        return False
    except TypeError:
        return False





