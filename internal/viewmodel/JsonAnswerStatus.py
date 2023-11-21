
from pydantic import BaseModel
from typing import Union, List

from internal.viewmodel.ContestViewModel import ContestUserStatementViewModel
from internal.viewmodel.UserViewModel import UserProfileLiteViewModel, UserPreviewViewModel
from internal.viewmodel.LeagueParticipationMembershipStatusViewModel import LeagueParticipationMembershipStatusMicroViewModel
from internal.viewmodel.NominationViewModel import NominationMicroViewModel
from internal.viewmodel.RegionViewModel import RegionMicroViewModel
from internal.viewmodel.UniversityViewModel import UniversityMicroViewModel
from internal.viewmodel.StatementViewModel import UserStatementViewModel, StatementPreviewViewModel
from internal.viewmodel.AdminViewModel import AdminProfileLiteViewModel
from internal.viewmodel.OnlineAuditoriumDataViewModel import OnlineAuditoriumDataLiteViewModel
from internal.viewmodel.OnlineAuditoriumMessageViewModel import OnlineAuditoriumChatNewViewModel
from internal.viewmodel.UserExpertStatementViewModel import UserExpertStatementPreviewsSearchDataViewModel
from internal.viewmodel.UserExpertStatementGradeViewModel import UserExpertStatementGradeEditViewModel

class JsonAnswerStatus(BaseModel):
    status: Union[str, None] = None
    errors: Union[str, None] = None
    is_auth: bool = False
    access_token: Union[str, None] = None
    forget_id: int = 0

    userProfileLiteViewModel: Union[UserProfileLiteViewModel, None] = None
    leagueParticipationMembershipStatusMicroViewModels: Union[List[LeagueParticipationMembershipStatusMicroViewModel], None] = None
    ...
    