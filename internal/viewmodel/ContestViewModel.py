
from pydantic import BaseModel
from typing import Union

class ContestMicroViewModel(BaseModel):
    id: int
    name: Union[str, None] = None


class ContestUserStatementViewModel(BaseModel):
    id: int
    name: Union[str, None] = None
    description: Union[str, None] = None
    is_visible: bool
    is_active: bool
    is_blocked_statement_edit: bool

    user_statement_is_start: bool
    user_statement_is_sent: bool