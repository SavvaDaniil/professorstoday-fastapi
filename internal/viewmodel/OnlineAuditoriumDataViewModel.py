from pydantic import BaseModel
from typing import Union
from datetime import datetime

class OnlineAuditoriumDataLiteViewModel(BaseModel):
	youtube_video_id: Union[str, None]
	is_open: bool = False
	is_available_upload_user_file: bool = False
	last_date_of_chat: Union[str, None]

