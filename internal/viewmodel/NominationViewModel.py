from pydantic import BaseModel
from typing import Union

class NominationMicroViewModel(BaseModel):
    id: int
    name: Union[str, None] = None