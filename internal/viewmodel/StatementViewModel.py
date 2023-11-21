from pydantic import BaseModel
from dataclasses import dataclass
from typing import Union, List

from internal.viewmodel.UserViewModel import UserMicroViewModel, UserProfileLiteViewModel
from internal.viewmodel.ContestViewModel import ContestMicroViewModel
from internal.viewmodel.NominationViewModel import NominationMicroViewModel

class StatementPreviewViewModel(BaseModel):
    id: int
    userMicroViewModel: Union[UserMicroViewModel, None] = None
    contestMicroViewModel: Union[ContestMicroViewModel, None] = None
    status: int
    photo_file_src: Union[str, None] = None
    nominationMicroViewModel: Union[NominationMicroViewModel, None] = None

    user_expert_statement_number: int
    user_expert_statement_appreciated_number: int

    date_of_add: Union[str, None] = None
    date_of_update: Union[str, None] = None


class UserStatementOtherFileViewModel(BaseModel):
    index: int
    src: Union[str, None] = None

class UserStatementApplicationsAndCharacteristicsFileViewModel(BaseModel):
    index: int
    src: Union[str, None] = None

class UserStatementViewModel(BaseModel):
    id: int
    user_id: int
    userProfileLiteViewModel: Union[UserProfileLiteViewModel, None] = None
    contest_id: int
    
    status: int

    #page 1
    statement_file_src: Union[str, None] = None
    photo_file_src: Union[str, None] = None
    nomination_id: int
    nominationMicroViewModel: Union[NominationMicroViewModel, None] = None


    #page 2
    education: Union[str, None] = None
    science_degree: Union[str, None] = None
    academic_status: Union[str, None] = None
    academic_status_another: Union[str, None] = None
    academic_rewards: Union[str, None] = None

    #page 3
    another_courses_and_other: Union[str, None] = None
    positions_outside_education: Union[str, None] = None
    seniority: Union[str, None] = None
    pedagogical_experience: Union[str, None] = None
    noncomerce_membership: Union[str, None] = None

    #page 4
    expert_of: Union[str, None] = None
    nir_niokr_membership: Union[str, None] = None
    patents_and_copyrights: Union[str, None] = None
    meetings_memberships_3_years: Union[str, None] = None
    magazine_publications_count: Union[str, None] = None
    rints_publications_count: Union[str, None] = None
    rints_citations_count: Union[str, None] = None
    hirsh_index: Union[str, None] = None
    published_textbooks_tutorials: Union[str, None] = None
    development_study_courses: Union[str, None] = None
    development_study_projects: Union[str, None] = None

    #page 5
    practice_oriented_teaching: Union[str, None] = None
    technical_and_presentation_equipment_use_degree: Union[str, None] = None
    internet_and_professional_activities_use_degree: Union[str, None] = None
    digital_training_courses: Union[str, None] = None
    study_improvement_information_resource: Union[str, None] = None
    innovative_approach_teaching_development: Union[str, None] = None
    interactive_teaching_methods: Union[str, None] = None
    graduated_masters_under_my_supervision: Union[str, None] = None
    graduated_students_under_my_supervision: Union[str, None] = None
    graduated_doctoral_under_my_supervision: Union[str, None] = None
    participant_in_international_educational_projects: Union[str, None] = None
    international_partnership_experience: Union[str, None] = None
    student_scientific_competitive_and_olympiad_movement_participant: Union[str, None] = None
    vocational_guidance_participant: Union[str, None] = None
    patriotic_projects_experience: Union[str, None] = None
    educational_activities_participation: Union[str, None] = None

    #page 6
    other_social_public_educational_work: Union[str, None] = None
    pedagogical_dynasty: Union[str, None] = None
    userStatementApplicationsAndCharacteristicsFileViewModels: Union[List[UserStatementApplicationsAndCharacteristicsFileViewModel], None] = None
    userStatementOtherFileViewModels: Union[List[UserStatementOtherFileViewModel], None] = None
    criminal_records: int
    professional_disqualification_records: int
    essay: Union[str, None] = None
    process_data_application_file_src: Union[str, None] = None


@dataclass
class UserStatementExcelRowViewModel():
    id: int

    username: Union[str, None] = None
    secondname: Union[str, None] = None
    firstname: Union[str, None] = None
    patronymic: Union[str, None] = None
    
    gender: Union[str, None] = None
    birthday: Union[str, None] = None
    telephone: Union[str, None] = None
    region: Union[str, None] = None
    address: Union[str, None] = None
    university: Union[str, None] = None
    position_not_university: Union[str, None] = None
    
    league_participation_is_membership: Union[str, None] = None
    league_participation_membership_status: Union[str, None] = None

    
    status: Union[str, None] = None

    #page 1
    nomination_name: Union[str, None] = None

    #page 2
    education: Union[str, None] = None
    science_degree: Union[str, None] = None
    academic_status: Union[str, None] = None
    academic_status_another: Union[str, None] = None
    academic_rewards: Union[str, None] = None

    #page 3
    another_courses_and_other: Union[str, None] = None
    positions_outside_education: Union[str, None] = None
    seniority: Union[str, None] = None
    pedagogical_experience: Union[str, None] = None
    noncomerce_membership: Union[str, None] = None

    #page 4
    expert_of: Union[str, None] = None
    nir_niokr_membership: Union[str, None] = None
    patents_and_copyrights: Union[str, None] = None
    meetings_memberships_3_years: Union[str, None] = None
    magazine_publications_count: Union[str, None] = None
    rints_publications_count: Union[str, None] = None
    rints_citations_count: Union[str, None] = None
    hirsh_index: Union[str, None] = None
    published_textbooks_tutorials: Union[str, None] = None
    development_study_courses: Union[str, None] = None
    development_study_projects: Union[str, None] = None

    #page 5
    ...

    #page 6
    ...
