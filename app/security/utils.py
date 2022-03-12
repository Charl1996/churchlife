import bcrypt


def hash_string(string_value: str) -> str:
    return bcrypt.hashpw(string_value, bcrypt.gensalt())


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password, hashed_password)


