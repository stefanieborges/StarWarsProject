from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.db import users_table

SECRET_KEY = "A4f$9vL@xPz!3nT#qW8bG^Y2eM6rJ0Kd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    try:
        response = users_table.get_item(Key={"username": username})
    except Exception as e:
        print("Erro ao acessar DynamoDB:", str(e))
        return None
    user = response.get("Item")
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Busca no DynamoDB
    try:
        response = users_table.get_item(Key={"username": username})
        user = response.get("Item")
    except Exception as e:
        print("Erro ao acessar DynamoDB:", str(e))
        raise HTTPException(status_code=500, detail="Erro ao buscar usuário")

    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user

