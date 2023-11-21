from pydantic import BaseModel
from typing import Union

class AdminLoginDTO(BaseModel):
    username: str
    password: str

class AdminProfileEditDTO(BaseModel):
    username: str
    position: Union[str, None]
    ...