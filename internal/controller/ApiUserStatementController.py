from xml.dom import ValidationErr
from fastapi import APIRouter, Request, Response, Depends, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Union, List
from logging import Logger

from internal.util.LoggerUtil import LoggerUtil
from internal.middleware.UserMiddleware import UserMiddleware
from internal.dto.StatementDTO import UserStatementEditDTO
from internal.facade.StatementFacade import StatementFacade
from internal.facade.NominationFacade import NominationFacade
from internal.facade.RegionFacade import RegionFacade
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus

routerUserStatement = APIRouter()

statementFacade: StatementFacade = StatementFacade()
logger: Logger = LoggerUtil.get()


@routerUserStatement.api_route('/contest/{contest_id_str}', response_model=JsonAnswerStatus, methods=['GET'])
def edit(request: Request, response: Response, contest_id_str: str):
    userMiddleware = UserMiddleware()
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    contest_id: int = 0
    try:
        contest_id = int(contest_id_str)
    except Exception:
        contest_id = 0

    try:
        nominationFacade: NominationFacade = NominationFacade()
        regionFacade: RegionFacade = RegionFacade()
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
        ...
        return jsonAnswerStatus
    except Exception as e:
        logger.error("GET /api/user/statement/contest/contest_id_str Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")
    return jsonAnswerStatus



@routerUserStatement.api_route('/contest/{contest_id_str}', response_model=JsonAnswerStatus, methods=['PUT'])
def update(
    request: Request, 
    response: Response, 
    contest_id_str: str, 
    
    id: int = Form(),
    status: int = Form(),

    #page 1
    statement_file: Union[UploadFile, None] = Form(None),
    photo_file: Union[UploadFile, None] = Form(None),
    nomination_id: int = Form(),

    
    #page 2
    ...
):
    userMiddleware = UserMiddleware()
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus

    contest_id: int = 0
    try:
        contest_id = int(contest_id_str)
    except Exception:
        contest_id = 0

    userStatementEditDTO: UserStatementEditDTO = UserStatementEditDTO(
        id = id,
        user_id = user_id,
        contest_id = contest_id,
        
        status = status,

        #page 1
        statement_file = statement_file,
        photo_file = photo_file,
        nomination_id = nomination_id,
        
        #page 2
        ...

        #page 3
        ...

        #page 4
        ...

        #page5
        ...

        #page 6
        ...
    )

    try:
        return statementFacade.update(user_id=user_id, userStatementEditDTO=userStatementEditDTO)
    except Exception as e:
        logger.error("PUT /api/user/statement/contest/" + contest_id_str + " Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")

@routerUserStatement.api_route('/contest/{contest_id_str}', response_model=JsonAnswerStatus, methods=['GET'])
def edit(request: Request, response: Response, contest_id_str: str):
    userMiddleware = UserMiddleware()
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    contest_id: int = 0
    try:
        contest_id = int(contest_id_str)
    except Exception:
        contest_id = 0
    #print("contest_id: " + str(contest_id))

    try:
        nominationFacade: NominationFacade = NominationFacade()
        regionFacade: RegionFacade = RegionFacade()
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
        ...
        return jsonAnswerStatus
    except Exception as e:
        logger.error("GET /api/user/statement/contest/contest_id_str Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")



@routerUserStatement.api_route('/{statement_id_str}/applications_and_characteristics_file/{file_index}', response_model=JsonAnswerStatus, methods=['DELETE'])
def delete_applications_and_characteristics_file(request: Request, response: Response, statement_id_str: str, file_index: str):
    userMiddleware = UserMiddleware()
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    statement_id: int = 0
    try:
        statement_id = int(statement_id_str)
    except Exception:
        statement_id = 0


    try:
        return JsonAnswerStatus(status="success") if statementFacade.delete_statement_applications_and_characteristics_by_index(user_id=user_id, statement_id=statement_id, file_index=file_index) else JsonAnswerStatus(status="error", errors="inknown")
    except Exception as e:
        logger.error("DELETE /api/user/statement/statement_id_str/applications_and_characteristics_file/file_index Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")

    

@routerUserStatement.api_route('/{statement_id_str}/other_file/{file_index}', response_model=JsonAnswerStatus, methods=['DELETE'])
def delete_other_file(request: Request, response: Response, statement_id_str: str, file_index: str):
    userMiddleware = UserMiddleware()
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    statement_id: int = 0
    try:
        statement_id = int(statement_id_str)
    except Exception:
        statement_id = 0

    try:
        return JsonAnswerStatus(status="success") if statementFacade.delete_other_file_by_index(user_id=user_id, statement_id=statement_id, file_index=file_index) else JsonAnswerStatus(status="error", errors="unknown")
    except Exception as e:
        logger.error("DELETE /api/user/statement/statement_id_str/other_file/file_index Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")


@routerUserStatement.api_route('/confirm/{statement_id_str}', response_model=JsonAnswerStatus, methods=['GET'])
def confirm_by_user(request: Request, response: Response, statement_id_str: str):
    userMiddleware = UserMiddleware()
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    statement_id: int = 0
    try:
        statement_id = int(statement_id_str)
    except Exception:
        statement_id = 0

    try:
        return statementFacade.confirm_by_user(user_id=user_id, statement_id=statement_id)
    except Exception as e:
        logger.error("GET /api/user/statement/confirm/statement_id_str Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")


@routerUserStatement.api_route('/contest/{contest_id_str}/withdraw', response_model=JsonAnswerStatus, methods=['GET'])
def withdraw_by_user(request: Request, response: Response, contest_id_str: str):
    userMiddleware = UserMiddleware()
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    contest_id: int = 0
    try:
        contest_id = int(contest_id_str)
    except Exception:
        contest_id = 0

    try:
        return statementFacade.withdraw_by_user(user_id=user_id, contest_id=contest_id)
    except Exception as e:
        logger.error("GET /api/user/statement/confirm/contest_id_str/withdraw Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")
    