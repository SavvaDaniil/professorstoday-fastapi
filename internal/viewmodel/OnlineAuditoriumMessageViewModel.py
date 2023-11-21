from pydantic import BaseModel
from typing import List, Union
from datetime import datetime

from internal.viewmodel.UserViewModel import UserMicroViewModel

class OnlineAuditoriumMessageLiteViewModel(BaseModel):
	id: int
	userMicroViewModel: Union[UserMicroViewModel, None]
	is_owner_of_request: bool
	message_content: Union[str, None]
	date_of_add: Union[str, None]

class OnlineAuditoriumChatNewViewModel(BaseModel):
	is_any_new: bool
	last_date_of_chat: Union[str, None]
	onlineAuditoriumMessageLiteViewModels: Union[List[OnlineAuditoriumMessageLiteViewModel], None] = []

