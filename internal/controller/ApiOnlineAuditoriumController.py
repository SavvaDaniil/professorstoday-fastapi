from xml.dom import ValidationErr
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from logging import Logger

from internal.middleware.UserMiddleware import UserMiddleware
from internal.facade.OnlineAuditoriumDataFacade import OnlineAuditoriumDataFacade
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus

from internal.util.LoggerUtil import LoggerUtil

routerOnlineAuditorium = APIRouter()

logger: Logger = LoggerUtil.get()
onlineAuditoriumDataFacade: OnlineAuditoriumDataFacade = OnlineAuditoriumDataFacade()
userMiddleware: UserMiddleware = UserMiddleware()

@routerOnlineAuditorium.api_route('/user/get_lite', response_model=JsonAnswerStatus, methods=['GET'])
def user_get_lite(request: Request, response: Response):
    
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        response.status_code = 200
        jsonAnswerStatus.onlineAuditoriumDataLiteViewModel = onlineAuditoriumDataFacade.get_lite()
    except Exception as e:
        response.status_code = 400
        logger.error("POST /api/online_auditorium/user/get_lite Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")
    return jsonAnswerStatus