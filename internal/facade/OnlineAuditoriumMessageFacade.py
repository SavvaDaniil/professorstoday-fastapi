from typing import List, Union
from datetime import datetime

from internal.Entities import OnlineAuditoriumMessage, User
from internal.facade.OnlineAuditoriumDataFacade import OnlineAuditoriumDataFacade
from internal.repository.OnlineAuditoriumMessageRepository import OnlineAuditoriumMessageRepository
from internal.repository.UserRepository import UserRepository
from internal.factory.UserFactory import UserFactory
from internal.viewmodel.OnlineAuditoriumDataViewModel import OnlineAuditoriumDataLiteViewModel
from internal.viewmodel.OnlineAuditoriumMessageViewModel import OnlineAuditoriumMessageLiteViewModel, OnlineAuditoriumChatNewViewModel
from internal.viewmodel.UserViewModel import UserMicroViewModel
from internal.custom_exception.UserCustomException import UserNotFoundException
from internal.custom_exception.OnlineAuditoriumException import OnlineAuditoriumClosedException
from internal.custom_exception.OnlineAuditoriumMessageException import OnlineAuditoriumMessageAddFailedException


class OnlineAuditoriumMessageFacade():

    def __init__(self) -> None:
        self.onlineAuditoriumMessageRepository: OnlineAuditoriumMessageRepository = OnlineAuditoriumMessageRepository()
        self.userRepository: UserRepository = UserRepository()
        self.onlineAuditoriumDataFacade: OnlineAuditoriumDataFacade = OnlineAuditoriumDataFacade()
        self.userFactory: UserFactory = UserFactory()

    def is_any_new_for_user_by_user_id(self, user_id: int, last_date_of_chat_str: Union[str, None]) -> OnlineAuditoriumChatNewViewModel:
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        onlineAuditoriumDataLiteViewModel: OnlineAuditoriumDataLiteViewModel = self.onlineAuditoriumDataFacade.get_lite()
        if not onlineAuditoriumDataLiteViewModel.is_open:
            raise OnlineAuditoriumClosedException()
        
        is_any_new: bool = False
        onlineAuditoriumMessageLiteViewModels: List[OnlineAuditoriumMessageLiteViewModel] = []

        if onlineAuditoriumDataLiteViewModel.last_date_of_chat is not None:
            if last_date_of_chat_str is None or onlineAuditoriumDataLiteViewModel.last_date_of_chat != last_date_of_chat_str:
                is_any_new = True
                onlineAuditoriumMessageLiteViewModels = self.__list_lite_for_user(user_owner_of_request=user)

        return OnlineAuditoriumChatNewViewModel(
            is_any_new=is_any_new,
            last_date_of_chat=onlineAuditoriumDataLiteViewModel.last_date_of_chat,
            onlineAuditoriumMessageLiteViewModels=onlineAuditoriumMessageLiteViewModels
        )


    def __list_lite_for_user(self, user_owner_of_request: User) -> List[OnlineAuditoriumMessageLiteViewModel]:

        onlineAuditoriumMessageLiteViewModels: List[OnlineAuditoriumMessageLiteViewModel] = []
        onlineAuditoriumMessages: List[OnlineAuditoriumMessage] = self.onlineAuditoriumMessageRepository.list_all_for_user()

        userMicroViewModel: Union[UserMicroViewModel, None]
        is_owner_of_request: bool = False
        for onlineAuditoriumMessage in onlineAuditoriumMessages:
            
            ...
            

            onlineAuditoriumMessageLiteViewModels.append(
                OnlineAuditoriumMessageLiteViewModel(
                    id=onlineAuditoriumMessage.id,
                    userMicroViewModel=userMicroViewModel,
                    is_owner_of_request=is_owner_of_request,
                    message_content=onlineAuditoriumMessage.message_text,
                    date_of_add=onlineAuditoriumMessage.date_of_add.strftime("%Y-%m-%d %H:%M:%S") if onlineAuditoriumMessage.date_of_add is not None else None
                )
            )
        
        return onlineAuditoriumMessageLiteViewModels

    def add(self, user_id: int, mesage_text: str) -> None:
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        datetime_now: datetime = datetime.now()
        onlineAuditoriumMessage: OnlineAuditoriumMessage = OnlineAuditoriumMessage()
        onlineAuditoriumMessage.user_id = user.id
        onlineAuditoriumMessage.message_text = mesage_text
        onlineAuditoriumMessage.is_deleted = False
        onlineAuditoriumMessage.date_of_add = datetime_now
        onlineAuditoriumMessage.date_of_update = datetime_now

        ...




        

