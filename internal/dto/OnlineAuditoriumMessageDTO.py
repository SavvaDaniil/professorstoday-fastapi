from pydantic import BaseModel
from typing import Union

class OnlineAuditoriumMessageNewByUserDTO(BaseModel):
    message_text: str


class OnlineAuditoriumChatData(BaseModel):
    last_date_of_chat: Union[str, None]
    ...