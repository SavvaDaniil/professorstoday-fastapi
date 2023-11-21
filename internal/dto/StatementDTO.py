from pydantic import BaseModel
from typing import Union, List
from fastapi import UploadFile


class StatementSearchDTO(BaseModel):
    page: int = 0
    query_string: Union[str, None]
    status: int = 0
    is_need_count: bool = False
    ...

class UserStatementEditDTO(BaseModel):
    id: int
    user_id: int
    contest_id: int
    
    status: int

    #page 1
    statement_file: Union[UploadFile, None] = None
    photo_file: Union[UploadFile, None] = None
    nomination_id: int

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