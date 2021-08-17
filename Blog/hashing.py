from passlib.context import CryptContext


class Hash:
    pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def crypt(cls, password: str):
        return cls.pwd_cxt.hash(password)
