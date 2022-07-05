from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verify_password(password: str, hashed_password: str) -> str:
    return PWD_CONTEXT.verify(password, hashed_password)
