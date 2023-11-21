
from pydantic import BaseModel
from typing import Union, List

class AdminProfileLiteViewModel(BaseModel):
    username: Union[str, None] = None
    position: Union[str, None] = None