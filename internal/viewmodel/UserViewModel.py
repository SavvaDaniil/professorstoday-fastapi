
from pydantic import BaseModel
from typing import Union, List

from internal.viewmodel.UniversityViewModel import UniversityMicroViewModel
from internal.viewmodel.RegionViewModel import RegionMicroViewModel
from internal.viewmodel.LeagueParticipationMembershipStatusViewModel import LeagueParticipationMembershipStatusMicroViewModel

class UserMicroViewModel(BaseModel):
    id: int
    username: Union[str, None] = None
    secondname: Union[str, None] = None
    firstname: Union[str, None] = None


class UserPreviewViewModel(BaseModel):
    id: int
    username: Union[str, None] = None
    ...


class UserProfileLiteViewModel(BaseModel):
    id: int
    username: Union[str, None] = None
    ...