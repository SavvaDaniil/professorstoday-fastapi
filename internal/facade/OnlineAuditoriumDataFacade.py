from typing import List, Union
from datetime import datetime

from internal.Entities import OnlineAuditoriumData
from internal.repository.OnlineAuditoriumDataRepository import OnlineAuditoriumDataRepository
from internal.viewmodel.OnlineAuditoriumDataViewModel import OnlineAuditoriumDataLiteViewModel


class OnlineAuditoriumDataFacade():

    def __init__(self) -> None:
        self.onlineAuditoriumDataRepository: OnlineAuditoriumDataRepository = OnlineAuditoriumDataRepository()

    def get_lite(self) -> OnlineAuditoriumDataLiteViewModel:

        onlineAuditoriumDatas: List[OnlineAuditoriumData] = self.onlineAuditoriumDataRepository.list_all()

        youtube_video_id: Union[str, None] = None
        is_open: bool = False
        is_available_upload_user_file: bool = False
        last_date_of_chat: Union[datetime, None] = None
        for onlineAuditoriumData in onlineAuditoriumDatas:
            ...

            if onlineAuditoriumData.name == "last_date_of_chat":
                last_date_of_chat = onlineAuditoriumData.date_value
                last_date_of_chat = last_date_of_chat.strftime("%Y-%m-%d %H:%M:%S")
        
        return OnlineAuditoriumDataLiteViewModel(
            youtube_video_id=youtube_video_id,
            is_open=is_open,
            is_available_upload_user_file=is_available_upload_user_file,
            last_date_of_chat=last_date_of_chat
        )


    def update_date_of_chat(self, new_date_of_chat: datetime) -> None:

        onlineAuditoriumData: OnlineAuditoriumData = self.onlineAuditoriumDataRepository.find_by_name(name="last_date_of_chat")
        if onlineAuditoriumData is None:
            return
        
        onlineAuditoriumData.date_value = new_date_of_chat
        self.onlineAuditoriumDataRepository.update(onlineAuditoriumData=onlineAuditoriumData)



