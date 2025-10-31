from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings


# ------------------------------------------------------------------------------
# --- Configuração de Segurança ---

# Contexto para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação que o FastAPI usará para extrair o token do header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ------------------------------------------------------------------------------
# --- Funções ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um novo token de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """Cria um novo refresh token com uma validade mais longa."""
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(data=data, expires_delta=expires)

def decode_token(token: str) -> Optional[str]:
    """Decodifica um token para extrair o nome de usuário."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

# --- Dependência para Proteger Endpoints ---

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependência para ser usada para endpoints protegidos.
    Extrai o token, válida e retorna o nome de usuário.
    Se o token for inválido, lança uma exceção HTTP 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = decode_token(token)
    if username is None:
        raise credentials_exception

    # Como retorno desta função, o nome de usuário é retornado.
    return username

def authenticate_user(db, username, password):
    """
    Busca o usuário no 'banco de dados' e verifica a senha.
    """
    if username in db:
        user_dict = db[username]
        if verify_password(password, user_dict["hashed_password"]):
            return user_dict
    return None

def get_current_user_from_refresh(token: str = Depends(oauth2_scheme)) -> str:
    # Esta função é similar à get_current_user, mas deve ser usada apenas para o endpoint de refresh.
    return get_current_user(token)