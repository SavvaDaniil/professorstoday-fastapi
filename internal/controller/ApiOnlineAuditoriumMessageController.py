from xml.dom import ValidationErr
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from logging import Logger

from internal.dto.OnlineAuditoriumMessageDTO import OnlineAuditoriumMessageNewByUserDTO, OnlineAuditoriumChatData
from internal.middleware.UserMiddleware import UserMiddleware
from internal.facade.OnlineAuditoriumMessageFacade import OnlineAuditoriumMessageFacade
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus

from internal.util.LoggerUtil import LoggerUtil

routerOnlineAuditoriumMessage = APIRouter()

logger: Logger = LoggerUtil.get()
onlineAuditoriumMessageFacade: OnlineAuditoriumMessageFacade = OnlineAuditoriumMessageFacade()
userMiddleware: UserMiddleware = UserMiddleware()

@routerOnlineAuditoriumMessage.api_route('/user/is_any_new', response_model=JsonAnswerStatus, methods=['POST'])
def user_is_any_new(request: Request, response: Response, onlineAuditoriumChatData: OnlineAuditoriumChatData):
    
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        jsonAnswerStatus.onlineAuditoriumChatNewViewModel = onlineAuditoriumMessageFacade.is_any_new_for_user_by_user_id(
            user_id=user_id,
            last_date_of_chat_str=onlineAuditoriumChatData.last_date_of_chat
        )
    except Exception as e:
        logger.error("POST /api/online_auditorium_message/user/is_any_new Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")
    return jsonAnswerStatus

@routerOnlineAuditoriumMessage.api_route('/user/add', response_model=JsonAnswerStatus, methods=['POST'])
def user_add(request: Request, response: Response, onlineAuditoriumMessageNewByUserDTO: OnlineAuditoriumMessageNewByUserDTO):
    
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        onlineAuditoriumMessageFacade.add(
            user_id=user_id,
            mesage_text=onlineAuditoriumMessageNewByUserDTO.message_text
        )
    except Exception as e:
        logger.error("POST /api/online_auditorium_message/user/add Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")
    return jsonAnswerStatus