from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(hashed_password, plain_password)