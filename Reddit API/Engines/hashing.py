from passlib.context import CryptContext

pwd_cxt= CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

class Hash():
    def hash(password):
       hashed_password= pwd_cxt.hash(password)
       return hashed_password

    def verify(hashed_password, plain_password):
      return pwd_cxt.verify(plain_password,hashed_password)