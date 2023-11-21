from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import base64

from internal.Entities import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserMiddleware():

    SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    def __init__(self):
        pass

    
    def get_current_user_id(self, request: Request, is_raise_exception: bool = False) -> int:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if token is None:
            if is_raise_exception:
                raise credentials_exception
            return 0
        token = token.replace("Bearer ", "")

        user_id: int = 0
        try:
            payload = jwt.decode(...)
            user_id_str: str = payload.get("XXXXXXXXXXXXXXXXXX")
            if user_id_str is None:
                if is_raise_exception:
                    raise credentials_exception
                else:
                    return 0
            user_id = int(user_id_str)
        except JWTError:
            if is_raise_exception:
                raise credentials_exception
            else:
                return 0
        return user_id

    def create_access_token(self, response: Response, user_id: int) -> str:
        to_encode = {"XXXXXXXXXXXXXXXXXXX": str(user_id)}
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        base64_bytes = base64.b64encode(self.SECRET_KEY.encode())
        encoded_jwt = jwt.encode(...)

        return encoded_jwt