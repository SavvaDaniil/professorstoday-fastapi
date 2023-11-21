
from pydantic import BaseModel
from typing import Union, List

from internal.viewmodel.UserViewModel import UserMicroViewModel, UserProfileLiteViewModel
from internal.viewmodel.NominationViewModel import NominationMicroViewModel
from internal.viewmodel.StatementViewModel import UserStatementViewModel

class UserExpertStatementGradePreviewViewModel(BaseModel):
    id: int
    statement_id: int
    nominationMicroViewModel: Union[NominationMicroViewModel, None]
    userMicroViewModel: Union[UserMicroViewModel, None]
    is_appreciated: bool

class UserExpertStatementGradeEditViewModel(BaseModel):
    id: int
    nominationMicroViewModel: Union[NominationMicroViewModel, None]
    userProfileLiteViewModel: Union[UserProfileLiteViewModel, None]
    userExpertMicroViewModel: Union[UserMicroViewModel, None] = None
    userStatementViewModel: Union[UserStatementViewModel, None]
    is_appreciated: bool
    
    #page 2
    education: int
    science_degree: int
    academic_status: int
    academic_status_another: int
    academic_rewards: int

    #page 3
    another_courses_and_other: int
    positions_outside_education: int
    seniority: int
    pedagogical_experience: int
    noncomerce_membership: int

    #page 4
    expert_of: int
    nir_niokr_membership: int
    patents_and_copyrights: int
    meetings_memberships_3_years: int
    magazine_publications_count: int
    rints_publications_count: int
    rints_citations_count: int
    hirsh_index: int
    published_textbooks_tutorials: int
    development_study_courses: int
    development_study_projects: int

    #page 5
    ...

    #page 6
    ...
