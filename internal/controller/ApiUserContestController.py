from xml.dom import ValidationErr
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from internal.middleware.UserMiddleware import UserMiddleware
from internal.facade.ContestFacade import ContestFacade
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus

routerUserContest = APIRouter()

@routerUserContest.api_route('/list', response_model=JsonAnswerStatus, methods=['GET'])
def list_active(request: Request, response: Response):
    userMiddleware = UserMiddleware()
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    contestFacade: ContestFacade = ContestFacade()
    return contestFacade.list_with_user_statement_for_user(user_id=user_id)


