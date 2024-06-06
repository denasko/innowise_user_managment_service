import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    return bcrypt.hashpw(password=password_bytes, salt=salt).decode()


def check_password(password: str, hashed_password: str) -> bool:
    print(password)
    print(hashed_password)
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password.encode())
