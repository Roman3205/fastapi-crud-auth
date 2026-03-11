from passlib.context import CryptContext

context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return context.verify(plain_password, hashed_password)