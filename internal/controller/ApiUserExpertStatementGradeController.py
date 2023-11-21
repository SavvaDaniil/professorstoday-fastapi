from xml.dom import ValidationErr
from fastapi import APIRouter, Request, Response, Depends, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Union, List
from logging import Logger

from internal.util.LoggerUtil import LoggerUtil
from internal.middleware.UserMiddleware import UserMiddleware
from internal.dto.UserExpertStatementGradeDTO import UserExpertStatementGradeEditDTO, UserExpertStatementGradeNewDTO
from internal.middleware.AdminMiddleware import AdminMiddleware
from internal.facade.StatementFacade import StatementFacade
from internal.facade.UserExpertStatementGradeFacade import UserExpertStatementGradeFacade
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus
from internal.custom_exception.UserCustomException import UserExpertNotFoundException, UserNotFoundException
from internal.custom_exception.UserExpertStatementGradeException import UserExpertStatementGradeNotFoundException, UserExpertStatementGradeAlreadyExistsException


routerUserExpertStatementGrade = APIRouter()

logger: Logger = LoggerUtil.get()
userExpertStatementGradeFacade: UserExpertStatementGradeFacade = UserExpertStatementGradeFacade()
statementFacade: StatementFacade = StatementFacade()
userMiddleware: UserMiddleware = UserMiddleware()


@routerUserExpertStatementGrade.api_route('/admin/add', response_model=JsonAnswerStatus, methods=['POST'])
def admin_add(request: Request, response: Response, userExpertStatementGradeNewDTO: UserExpertStatementGradeNewDTO):
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")

    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        userExpertStatementGradeFacade.add(userExpertStatementGradeNewDTO=userExpertStatementGradeNewDTO)
    except UserNotFoundException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except UserExpertNotFoundException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except UserExpertStatementGradeAlreadyExistsException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except Exception as e:
        logger.error("PUT /api/user_expert_statement_grade/expert/user_expert_statement_grade_id_str Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")

    return jsonAnswerStatus


@routerUserExpertStatementGrade.api_route('/expert', response_model=JsonAnswerStatus, methods=['PUT'])
def expert_get(request: Request, response: Response, userExpertStatementGradeEditDTO: UserExpertStatementGradeEditDTO):
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus

    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")

    try:
        userExpertStatementGradeFacade.update(
            user_id=user_id,
            userExpertStatementGradeEditDTO=userExpertStatementGradeEditDTO
        )
    except UserExpertStatementGradeNotFoundException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except Exception as e:
        logger.error("PUT /api/user_expert_statement_grade/expert/user_expert_statement_grade_id_str Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")

    return jsonAnswerStatus