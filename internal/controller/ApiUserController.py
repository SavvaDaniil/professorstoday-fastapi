from xml.dom import ValidationErr
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from logging import Logger

from internal.middleware.UserMiddleware import UserMiddleware
from internal.middleware.AdminMiddleware import AdminMiddleware
from internal.util.LoggerUtil import LoggerUtil
from internal.facade.UserFacade import UserFacade
from internal.facade.RegionFacade import RegionFacade
from internal.facade.UniversityFacade import UniversityFacade
from internal.facade.StatementFacade import StatementFacade
from internal.facade.LeagueParticipationMembershipStatusFacade import LeagueParticipationMembershipStatusFacade
from internal.dto.UserDTO import UserLoginDTO, UserRegistrationDTO, UserProfileEditDTO, UserForgetDTO, UserSearchDTO, UserExpertSetupNewDTO
from internal.custom_exception.UserCustomException import UserNotFoundException, UserNotExpertException, UserNotExpertSetupedException, UserProfileNotFilledException, UserExpertNoChoosenNominationsException
from internal.viewmodel.UserViewModel import UserProfileLiteViewModel
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus

routerUser = APIRouter()

logger: Logger = LoggerUtil.get()
userMiddleware: UserMiddleware = UserMiddleware()
userFacade: UserFacade = UserFacade()
statementFacade: StatementFacade = StatementFacade()
    

@routerUser.api_route('/expert/{user_expert_statement_grade_id_str}', response_model=JsonAnswerStatus, methods=['GET'])
def expert_get(request: Request, response: Response, user_expert_statement_grade_id_str: str):
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    user_expert_statement_grade_id: int = 0
    try:
        user_expert_statement_grade_id = int(user_expert_statement_grade_id_str)
    except Exception:
        user_expert_statement_grade_id = 0

    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    leagueParticipationMembershipStatusFacade: LeagueParticipationMembershipStatusFacade = LeagueParticipationMembershipStatusFacade()
    regionFacade: RegionFacade = RegionFacade()
    universityFacade: UniversityFacade = UniversityFacade()

    try:
        jsonAnswerStatus.userExpertStatementGradeEditViewModel = statementFacade.expert_get_grade_by_id(
            user_expert_id=user_id,
            user_expert_statement_grade_id=user_expert_statement_grade_id
        )
        jsonAnswerStatus.leagueParticipationMembershipStatusMicroViewModels=leagueParticipationMembershipStatusFacade.list_micro_for_user()
        jsonAnswerStatus.regionMicroViewModels=regionFacade.list_all_micro()
        jsonAnswerStatus.universityMicroViewModels = universityFacade.list_all_micro()
    except UserNotFoundException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except UserNotExpertException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except UserExpertNoChoosenNominationsException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except Exception as e:
        logger.error("GET /api/user/expert/user_expert_statement_grade_id_str Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")

    return jsonAnswerStatus


@routerUser.api_route('/expert/setup', response_model=JsonAnswerStatus, methods=['POST'])
def expert_get(request: Request, response: Response, userExpertSetupNewDTO: UserExpertSetupNewDTO):
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        userFacade.expert_setup(user_id=user_id, userExpertSetupNewDTO=userExpertSetupNewDTO)
    except UserNotFoundException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except UserNotExpertException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except UserExpertNoChoosenNominationsException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except Exception as e:
        logger.error("POST /api/user/expert/setup Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")

    return jsonAnswerStatus

@routerUser.api_route('/expert', response_model=JsonAnswerStatus, methods=['GET'])
def expert_get(request: Request, response: Response):
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
    try:
        jsonAnswerStatus.userExpertStatementPreviewsSearchDataViewModel = userFacade.expert_list_of_statement_previews_for_user_expert(user_id=user_id)
    except UserNotExpertException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except UserNotExpertSetupedException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except UserProfileNotFilledException as e:
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors=str(e))
    except Exception as e:
        logger.error("GET /api/user/expert Exception: " + str(e))
        jsonAnswerStatus = JsonAnswerStatus(status="error", errors="unknown")

    return jsonAnswerStatus


@routerUser.get("", response_model=JsonAnswerStatus)
def index(request: Request, response: Response):
    user_id: int = userMiddleware.get_current_user_id(request=request)
    response.status_code = 200 if user_id != 0 else 401
    jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(
        status=("success" if user_id != 0 else "error"),
        errors=(None if user_id != 0 else "not_auth")
    )
    return jsonAnswerStatus


@routerUser.api_route('/registration', response_model=JsonAnswerStatus, methods=['POST', 'HEAD'])
def login(request: Request, response: Response, userRegistrationDTO: UserRegistrationDTO):
    try:
        return userFacade.registration(response=response, userRegistrationDTO=userRegistrationDTO)
    except Exception as e:
        logger.error("POST /api/user/registration Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")

@routerUser.api_route('/login', response_model=JsonAnswerStatus, methods=['POST'])
def login(request: Request, response: Response, userLoginDTO: UserLoginDTO):
    try:
        return userFacade.login(response=response, userLoginDTO=userLoginDTO)
    except Exception as e:
        logger.error("POST /api/user/login Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")

@routerUser.api_route('/profile', response_model=JsonAnswerStatus, methods=['GET'])
def profile_get(request: Request, response: Response):
    #logging.debug("api user profile get")
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    leagueParticipationMembershipStatusFacade: LeagueParticipationMembershipStatusFacade = LeagueParticipationMembershipStatusFacade()
    regionFacade: RegionFacade = RegionFacade()
    universityFacade: UniversityFacade = UniversityFacade()
    try:
        userProfileLiteViewModel: UserProfileLiteViewModel = userFacade.profile_get(user_id=user_id)
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(
            status="success",
            is_auth=True,
            userProfileLiteViewModel=userProfileLiteViewModel,
            ...
        )
        return jsonAnswerStatus
    except UserNotFoundException:
        return JsonAnswerStatus(status="error", errors="user not found")
    except Exception as e:
        logger.error("GET /api/user/profile Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")
    

@routerUser.api_route('/profile', response_model=JsonAnswerStatus, methods=['PUT'])
def profile_update(request: Request, response: Response, userProfileEditDTO: UserProfileEditDTO):
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 401
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="error", errors="not_auth")
        return jsonAnswerStatus
    
    try:
        return userFacade.profile_update(response=response, user_id=user_id, userProfileEditDTO=userProfileEditDTO)
    except Exception as e:
        logger.error("PUT /api/user/profile Exception: " + str(e))
        return JsonAnswerStatus(status="error", errors="unknown")




@routerUser.api_route('/forget', response_model=JsonAnswerStatus, methods=['POST'])
def profile_get(request: Request, response: Response, userForgetDTO: UserForgetDTO):
    
    try:
        return userFacade.forget(
            response=response,
            userForgetDTO=userForgetDTO
        )
    except UserNotFoundException:
        return JsonAnswerStatus(status="error", errors="unknown")
