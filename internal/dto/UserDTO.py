from pydantic import BaseModel
from typing import Union, List

class UserExpertSetupNewDTO(BaseModel):
    nomination_ids: List[int]

class UserSearchDTO(BaseModel):
    page: int = 0
    query_string: Union[str, None]
    is_need_count: bool = False
    is_only_experts: bool = False

class UserForgetDTO(BaseModel):
    step: int
    forget_id: int = 0
    username: Union[str, None]
    code: Union[str, None]

class UserLoginDTO(BaseModel):
    username: str
    password: str

class UserRegistrationDTO(BaseModel):
    username: str
    firstname: str
    secondname: str
    patronymic: str
    password: str

class UserProfileEditDTO(BaseModel):
    username: str
    firstname: Union[str, None]
    ...

class UserEditDTO(BaseModel):
    id: int
    username: str
    firstname: Union[str, None]
    ...