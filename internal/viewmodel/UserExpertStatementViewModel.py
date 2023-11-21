
from pydantic import BaseModel
from typing import Union, List

from internal.viewmodel.NominationViewModel import NominationMicroViewModel
from internal.viewmodel.UserExpertStatementGradeViewModel import UserExpertStatementGradePreviewViewModel

class UserExpertStatementPreviewsSearchDataViewModel(BaseModel):
    is_expert_setuped: bool
    nominationMicroViewModels: Union[List[NominationMicroViewModel], None]
    userExpertStatementGradePreviewViewModels: Union[List[UserExpertStatementGradePreviewViewModel], None] = None