from xml.dom import ValidationErr
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from logging import Logger

from internal.middleware.AdminMiddleware import AdminMiddleware
from internal.facade.AdminFacade import AdminFacade
from internal.facade.UserFacade import UserFacade
from internal.facade.RegionFacade import RegionFacade
from internal.facade.UniversityFacade import UniversityFacade
from internal.facade.StatementFacade import StatementFacade
from internal.facade.NominationFacade import NominationFacade
from internal.facade.UserExpertStatementGradeFacade import UserExpertStatementGradeFacade
from internal.facade.LeagueParticipationMembershipStatusFacade import LeagueParticipationMembershipStatusFacade
from internal.dto.AdminDTO import AdminLoginDTO, AdminProfileEditDTO
from internal.dto.UserDTO import UserSearchDTO, UserEditDTO
from internal.dto.StatementDTO import StatementSearchDTO
from internal.custom_exception.AdminCustomException import AdminLoginFailedException
from internal.custom_exception.UserCustomException import UserExpertFoundedTooMuchException
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus

from internal.util.LoggerUtil import LoggerUtil

routerAdmin = APIRouter()

logger: Logger = LoggerUtil.get()
adminFacade: AdminFacade = AdminFacade()
userFacade: UserFacade = UserFacade()
statementFacade: StatementFacade = StatementFacade()
regionFacade: RegionFacade = RegionFacade()
leagueParticipationMembershipStatusFacade: LeagueParticipationMembershipStatusFacade = LeagueParticipationMembershipStatusFacade()
universityFacade: UniversityFacade = UniversityFacade()
nominationFacade: NominationFacade = NominationFacade()
userExpertStatementGradeFacade: UserExpertStatementGradeFacade = UserExpertStatementGradeFacade()
    
@routerAdmin.api_route('/statement/{statement_id_str}', response_model=JsonAnswerStatus, methods=['GET'])
def statement_get(request: Request, response: Response, statement_id_str: str):
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")
    
    statement_id: int = 0
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        statement_id = int(statement_id_str)
        jsonAnswerStatus.userStatementViewModel = statementFacade.get_for_admin_by_id(statement_id=statement_id)
        jsonAnswerStatus.nominationMicroViewModels = nominationFacade.list_micro()
        jsonAnswerStatus.leagueParticipationMembershipStatusMicroViewModels=leagueParticipationMembershipStatusFacade.list_micro_for_user()
        jsonAnswerStatus.regionMicroViewModels=regionFacade.list_all_micro()
        ...

    except Exception as e:
        logger.error("POST /api/statement/search Exception: " + str(e))
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")
    return jsonAnswerStatus

@routerAdmin.api_route('/statement/search', response_model=JsonAnswerStatus, methods=['POST'])
def statement_search(request: Request, response: Response, statementSearchDTO: StatementSearchDTO):
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")
    
    try:
        return statementFacade.search(statementSearchDTO=statementSearchDTO)
    except Exception as e:
        logger.error("POST /api/statement/search Exception: " + str(e))
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")
        return jsonAnswerStatus
    
@routerAdmin.api_route('/user/search_experts', response_model=JsonAnswerStatus, methods=['POST'])
def search_experts(request: Request, response: Response, userSearchDTO: UserSearchDTO):
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")
    
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        #return userFacade.search(userSearchDTO=userSearchDTO)
        jsonAnswerStatus.userPreviewViewModels = userFacade.search_expert(userSearchDTO=userSearchDTO)

    except UserExpertFoundedTooMuchException as e:
        logger.error("POST /api/user/search_expert UserExpertFoundedTooMuchException: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except Exception as e:
        logger.error("POST /api/user/search_expert Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")
    return jsonAnswerStatus


@routerAdmin.api_route('/user/profile', response_model=JsonAnswerStatus, methods=['PUT'])
def user_update(request: Request, response: Response, userEditDTO: UserEditDTO):
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")

    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        userFacade.edit_by_admin(userEditDTO=userEditDTO)
    except Exception as e:
        logger.error("PUT /api/admin/user/profile Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")

    return jsonAnswerStatus


@routerAdmin.api_route('/user/{user_id_str}', response_model=JsonAnswerStatus, methods=['GET'])
def search(request: Request, response: Response, user_id_str: str):
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")
    
    leagueParticipationMembershipStatusFacade: LeagueParticipationMembershipStatusFacade = LeagueParticipationMembershipStatusFacade()
    regionFacade: RegionFacade = RegionFacade()
    universityFacade: UniversityFacade = UniversityFacade()

    user_id: int = 0
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        user_id = int(user_id_str)
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(
            status="success",
            userProfileLiteViewModel=userFacade.profile_get(user_id=user_id),
            ...
        )
    except Exception as e:
        logger.error("POST /api/user/search Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")

    return jsonAnswerStatus
    
@routerAdmin.api_route('/user/search', response_model=JsonAnswerStatus, methods=['POST'])
def search(request: Request, response: Response, userSearchDTO: UserSearchDTO):
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")
    
    try:
        return userFacade.search(userSearchDTO=userSearchDTO)
    except Exception as e:
        logger.error("POST /api/user/search Exception: " + str(e))
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")
        return jsonAnswerStatus

@routerAdmin.api_route("", response_model=JsonAnswerStatus, methods=["GET"])
def index(request: Request, response: Response) -> JSONResponse:
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    response.status_code = 200 if admin_id != 0 else 401
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(
        status=("success" if admin_id != 0 else "error"),
        errors=(None if admin_id != 0 else "not_auth")
    )
    return jsonAnswerStatus

@routerAdmin.api_route("/login", response_model=JsonAnswerStatus, methods=["POST"])
def index(request: Request, response: Response, adminLoginDTO: AdminLoginDTO) -> JSONResponse:

    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        jsonAnswerStatus.access_token = adminFacade.login(response=response, adminLoginDTO=adminLoginDTO)
    except AdminLoginFailedException as e:
        jsonAnswerStatus.status = "error"
        jsonAnswerStatus.errors = str(e)
    except Exception as e:
        print("/api/admin/login Exception: ", str(e))
        jsonAnswerStatus.status = "error"
        jsonAnswerStatus.errors = "unknown"
    return jsonAnswerStatus

@routerAdmin.api_route("/profile", response_model=JsonAnswerStatus, methods=["GET"])
def profile_get(request: Request, response: Response) -> JSONResponse:
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")

    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        jsonAnswerStatus.adminProfileLiteViewModel = adminFacade.get_profile_by_id(admin_id=admin_id)
    except Exception as e:
        jsonAnswerStatus.status = "error"
        jsonAnswerStatus.errors = str(e)
    return jsonAnswerStatus

@routerAdmin.api_route("/profile", response_model=JsonAnswerStatus, methods=["PUT"])
def profile_put(request: Request, response: Response, adminProfileEditDTO: AdminProfileEditDTO) -> JSONResponse:
    adminMiddleware: AdminMiddleware = AdminMiddleware()
    admin_id: int = adminMiddleware.get_current_admin_id(request=request)
    if admin_id == 0:
        response.status_code = 401
        return JsonAnswerStatus(status="errors", errors="not_auth")

    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        jsonAnswerStatus = adminFacade.profile_update(
            response=response,
            admin_id=admin_id,
            adminProfileEditDTO=adminProfileEditDTO 
        )
    except Exception as e:
        jsonAnswerStatus.status = "error"
        jsonAnswerStatus.errors = str(e)
    return jsonAnswerStatus