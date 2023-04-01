from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
