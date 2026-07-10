from fastapi.security import OAuth2PasswordBearer

#Extract token automatically
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)