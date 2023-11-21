from pydantic import BaseModel
from typing import Union, List

class UserExpertStatementGradeNewDTO(BaseModel):
    user_expert_id: int
    statement_id: int

class UserExpertStatementGradeEditDTO(BaseModel):
    id: int

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