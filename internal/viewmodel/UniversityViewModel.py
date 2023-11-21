

from pydantic import BaseModel
from typing import Union

class UniversityMicroViewModel(BaseModel):
    id: int
    name: Union[str, None] = None