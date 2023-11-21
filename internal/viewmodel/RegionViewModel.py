from pydantic import BaseModel
from typing import Union

class RegionMicroViewModel(BaseModel):
    id: int
    name: Union[str, None] = None
