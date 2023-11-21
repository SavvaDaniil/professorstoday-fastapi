from sqlalchemy import Column, Integer, Boolean, String, Date, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#Base = ApplicationDbContext.Base
Base = declarative_base()


class LeagueParticipationMembershipStatus(Base):
    __tablename__ = "league_participation_membership_status"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    name = Column("name", String(255), nullable=True)
    is_active = Column("is_active", Integer, nullable=False, default="0")

    users = relationship("User", back_populates="league_participation_membership_status")


class OnlineAuditoriumData(Base):
    __tablename__ = "online_auditorium_data"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    name = Column("name", String(255), nullable=True)
    str_value = Column("str_value", String(255), nullable=True)
    int_value = Column("int_value", Integer, nullable=False, default="0")
    date_value = Column("date_value", DateTime, nullable=True)
    

class Admin(Base):
    __tablename__ = "admin"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    username = Column("username", String(255))
    password = Column("password", String(255))
    auth_key = Column("auth_key", String(255))
    access_token = Column("access_token", String(255))
    level = Column("level", Integer, nullable=False, default="0")
    active = Column("active", Integer, nullable=False, default="0")
    position = Column("position", String(255))

    date_of_add = Column("date_of_add", DateTime)
    date_of_last_update_profile = Column("date_of_last_update_profile", DateTime)


class University(Base):
    __tablename__ = "university"

    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    prev_id = Column("prev_id", Integer, nullable=False, default="0")
    name = Column("name", String(1024))

    users = relationship("User", back_populates="university")

    
class User(Base):
    __tablename__ = "user"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    username = Column("username", String(255))
    password = Column("password", String(255))
    auth_key = Column("auth_key", String(255))
    access_token = Column("access_token", String(255))
    roles = Column("roles", String(255))
    active = Column("active", Integer, nullable=False, default="0")
    secondname = Column("secondname", String(255))
    firstname = Column("firstname", String(255))
    patronymic = Column("patronymic", String(255))
    gender = Column("gender", Integer, nullable=False, default="0")
    birthday = Column("birthday", Date)
    telephone = Column("telephone", String(255))
    
    region_id = Column("region_id", Integer, ForeignKey("region.id"))
    region = relationship("Region", back_populates="users", lazy="joined")

    address = Column("address", Text)
    position_university = Column("position_university", Text)

    university_id = Column("university_id", Integer, ForeignKey("university.id"))
    university = relationship("University", back_populates="users", lazy="joined")

    position_not_university = Column("position_not_university", Text)

    league_participation_is_membership = Column("league_participation_is_membership", Integer, nullable=False, default="0")

    league_participation_membership_status_str = Column("league_participation_membership_status_str", String(255))

    league_participation_membership_status_id = Column("league_participation_membership_status_id", Integer, ForeignKey("league_participation_membership_status.id"))
    league_participation_membership_status = relationship("LeagueParticipationMembershipStatus", back_populates="users", lazy="joined")


    is_banned = Column("is_banned", Boolean)
    persmissions = Column("persmissions", Integer, nullable=False, default=0)
    date_of_add = Column("date_of_add", DateTime)
    date_of_last_update_profile = Column("date_of_last_update_profile", DateTime)
    forget_count = Column("forget_count", Integer, nullable=False, default=0)
    forget_code = Column("forget_code", String(6))
    forget_date_of_last_try = Column("forget_date_of_last_try", DateTime)

    statements = relationship("Statement", back_populates="user")
    online_auditorium_messages = relationship("OnlineAuditoriumMessage", back_populates="user")

    is_expert = Column("is_expert", Boolean, default=False)
    is_expert_setuped = Column("is_expert_setuped", Boolean, default=False)

    user_expert_statements = relationship("UserExpertStatementGrade", back_populates="user_expert")


class Contest(Base):
    __tablename__ = "contest"

    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    name = Column("name", String(255))
    description = Column("description", Text)
    is_visible = Column("is_visible", Boolean)
    is_active = Column("is_active", Boolean)
    is_blocked_statement_edit = Column("is_blocked_statement_edit", Boolean)

    statements = relationship("Statement", back_populates="contest")

class Nomination(Base):
    __tablename__ = "nomination"

    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    name = Column("name", String(255))

    statements = relationship("Statement", back_populates="nomination")

class Region(Base):
    __tablename__ = "region"

    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    name = Column("name", String(255))
    order_in_list = Column("order_in_list", Integer, nullable=False, default="0")

    users = relationship("User", back_populates="region")
    statements = relationship("Statement", back_populates="region")





class ScientificDirection(Base):
    __tablename__ = "scientific_direction"

    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    name = Column("name", String(255))

    statements = relationship("Statement", back_populates="scientific_direction")


class Statement(Base):
    __tablename__ = "statement"

    id = Column("id", Integer, primary_key = True, index=True, unique = True)

    user_id = Column("user_id", Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="statements", lazy="joined")

    contest_id = Column("contest_id", Integer, ForeignKey("contest.id"))
    contest = relationship("Contest", back_populates="statements", lazy="joined")

    nomination_id = Column("nomination_id", Integer, ForeignKey("nomination.id"))
    nomination = relationship("Nomination", back_populates="statements", lazy="joined")

    scientific_direction_id = Column("scientific_direction_id", Integer, ForeignKey("scientific_direction.id"))
    scientific_direction = relationship("ScientificDirection", back_populates="statements")

    status = Column("status", Integer, nullable=False, default="0")

    #page 1
    league_participation_is_membership = Column("league_participation_is_membership", Integer, nullable=False, default="0")
    league_participation_membership_status = Column("league_participation_membership_status", String(255))

    username = Column("username", String(255))
    secondname = Column("secondname", String(255))
    firstname = Column("firstname", String(255))
    patronymic = Column("patronymic", String(255))
    gender = Column("gender", Integer, nullable=False, default="0")
    birthday = Column("birthday", Date)
    telephone = Column("telephone", String(255))
    
    region_id = Column("region_id", Integer, ForeignKey("region.id"))
    region = relationship("Region", back_populates="statements")

    address = Column("address", Text)

    position_university = Column("position_university", Text)
    position_not_university = Column("position_not_university", Text)

    #page 2
    education = Column("education", Text)
    science_degree = Column("science_degree", Text)
    academic_status = Column("academic_status", Text)
    academic_status_another = Column("academic_status_another", Text)
    academic_rewards = Column("academic_rewards", Text)

    #page 3
    another_courses_and_other = Column("another_courses_and_other", Text)
    positions_outside_education = Column("positions_outside_education", Text)
    seniority = Column("seniority", Text)
    pedagogical_experience = Column("pedagogical_experience", Text)
    noncomerce_membership = Column("noncomerce_membership", Text)

    #page 4
    expert_of = Column("expert_of", Text)
    nir_niokr_membership = Column("nir_niokr_membership", Text)
    patents_and_copyrights = Column("patents_and_copyrights", Text)
    meetings_memberships_3_years = Column("meetings_memberships_3_years", Text)
    magazine_publications_count = Column("magazine_publications_count", Text)
    rints_publications_count = Column("rints_publications_count", Text)
    rints_citations_count = Column("rints_citations_count", Text)
    hirsh_index = Column("hirsh_index", Text)
    published_textbooks_tutorials = Column("published_textbooks_tutorials", Text)
    development_study_courses = Column("development_study_courses", Text)
    development_study_projects = Column("development_study_projects", Text)

    #page 5
    practice_oriented_teaching = Column("practice_oriented_teaching", Text)
    technical_and_presentation_equipment_use_degree = Column("technical_and_presentation_equipment_use_degree", Text)
    internet_and_professional_activities_use_degree = Column("internet_and_professional_activities_use_degree", Text)
    digital_training_courses = Column("digital_training_courses", Text)
    study_improvement_information_resource = Column("study_improvement_information_resource", Text)
    innovative_approach_teaching_development = Column("innovative_approach_teaching_development", Text)
    interactive_teaching_methods = Column("interactive_teaching_methods", Text)
    graduated_masters_under_my_supervision = Column("graduated_masters_under_my_supervision", Text)
    graduated_students_under_my_supervision = Column("graduated_students_under_my_supervision", Text)
    graduated_doctoral_under_my_supervision = Column("graduated_doctoral_under_my_supervision", Text)
    participant_in_international_educational_projects = Column("participant_in_international_educational_projects", Text)
    international_partnership_experience = Column("international_partnership_experience", Text)
    student_scientific_competitive_and_olympiad_movement_participant = Column("student_scientific_competitive_and_olympiad_movement_participant", Text)
    vocational_guidance_participant = Column("vocational_guidance_participant", Text)
    patriotic_projects_experience = Column("patriotic_projects_experience", Text)
    educational_activities_participation = Column("educational_activities_participation", Text)

    #page 6
    other_social_public_educational_work = Column("other_social_public_educational_work", Text)
    pedagogical_dynasty = Column("pedagogical_dynasty", Text)
    criminal_records = Column("criminal_records", Integer, nullable=False, default="0")
    professional_disqualification_records = Column("professional_disqualification_records", Integer, nullable=False, default="0")
    essay = Column("essay", Text)

    #XXXXXXXXXXXXXXXX = Column("XXXXXXXXXXXXXXXX", Text)
    #XXXXXXXXXXXXXXXX = Column("XXXXXXXXXXXXXXXX", Text)
    #XXXXXXXXXXXXXXXX = Column("XXXXXXXXXXXXXXXX", Text)


    date_of_add = Column("date_of_add", DateTime)
    date_of_update = Column("date_of_update", DateTime)
    
    is_appreciated = Column("is_appreciated", Boolean, nullable=False, default="0")

    user_expert_statement_grades = relationship("UserExpertStatementGrade", back_populates="statement")


class OnlineAuditoriumMessage(Base):
    __tablename__ = "online_auditorium_message"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    
    user_id = Column("user_id", Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="online_auditorium_messages", lazy="joined")

    message_text = Column("message_text", Text, nullable=True)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default="0")
    date_of_add = Column("date_of_add", DateTime, nullable=True)
    date_of_update = Column("date_of_update", DateTime, nullable=True)


class UserExpertStatementGrade(Base):
    __tablename__ = "user_expert_statement_grade"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    
    user_expert_id = Column("user_expert_id", Integer, ForeignKey("user.id"))
    user_expert = relationship("User", back_populates="user_expert_statements", lazy="joined")
    
    statement_id = Column("statement_id", Integer, ForeignKey("statement.id"))
    statement = relationship("Statement", back_populates="user_expert_statement_grades", lazy="joined")

    is_appreciated = Column("is_appreciated", Boolean, nullable=False, default=False)

    date_of_add = Column("date_of_add", DateTime, nullable=True)
    date_of_update = Column("date_of_update", DateTime, nullable=True)

    #page 2
    education = Column("education", Integer, nullable=False, default="-1")
    science_degree = Column("science_degree", Integer, nullable=False, default="-1")
    academic_status = Column("academic_status", Integer, nullable=False, default="-1")
    academic_status_another = Column("academic_status_another", Integer, nullable=False, default="-1")
    academic_rewards = Column("academic_rewards", Integer, nullable=False, default="-1")

    #page 3
    another_courses_and_other = Column("another_courses_and_other", Integer, nullable=False, default="-1")
    positions_outside_education = Column("positions_outside_education", Integer, nullable=False, default="-1")
    seniority = Column("seniority", Integer, nullable=False, default="-1")
    pedagogical_experience = Column("pedagogical_experience", Integer, nullable=False, default="-1")
    noncomerce_membership = Column("noncomerce_membership", Integer, nullable=False, default="-1")

    #page 4
    expert_of = Column("expert_of", Integer, nullable=False, default="-1")
    nir_niokr_membership = Column("nir_niokr_membership", Integer, nullable=False, default="-1")
    patents_and_copyrights = Column("patents_and_copyrights", Integer, nullable=False, default="-1")
    meetings_memberships_3_years = Column("meetings_memberships_3_years", Integer, nullable=False, default="-1")
    magazine_publications_count = Column("magazine_publications_count", Integer, nullable=False, default="-1")
    rints_publications_count = Column("rints_publications_count", Integer, nullable=False, default="-1")
    rints_citations_count = Column("rints_citations_count", Integer, nullable=False, default="-1")
    hirsh_index = Column("hirsh_index", Integer, nullable=False, default="-1")
    published_textbooks_tutorials = Column("published_textbooks_tutorials", Integer, nullable=False, default="-1")
    development_study_courses = Column("development_study_courses", Integer, nullable=False, default="-1")
    development_study_projects = Column("development_study_projects", Integer, nullable=False, default="-1")

    #page 5
    practice_oriented_teaching = Column("practice_oriented_teaching", Integer, nullable=False, default="-1")
    technical_and_presentation_equipment_use_degree = Column("technical_and_presentation_equipment_use_degree", Integer, nullable=False, default="-1")
    internet_and_professional_activities_use_degree = Column("internet_and_professional_activities_use_degree", Integer, nullable=False, default="-1")
    digital_training_courses = Column("digital_training_courses", Integer, nullable=False, default="-1")
    study_improvement_information_resource = Column("study_improvement_information_resource", Integer, nullable=False, default="-1")
    innovative_approach_teaching_development = Column("innovative_approach_teaching_development", Integer, nullable=False, default="-1")
    interactive_teaching_methods = Column("interactive_teaching_methods", Integer, nullable=False, default="-1")
    graduated_masters_under_my_supervision = Column("graduated_masters_under_my_supervision", Integer, nullable=False, default="-1")
    graduated_students_under_my_supervision = Column("graduated_students_under_my_supervision", Integer, nullable=False, default="-1")
    graduated_doctoral_under_my_supervision = Column("graduated_doctoral_under_my_supervision", Integer, nullable=False, default="-1")
    participant_in_international_educational_projects = Column("participant_in_international_educational_projects", Integer, nullable=False, default="-1")
    international_partnership_experience = Column("international_partnership_experience", Integer, nullable=False, default="-1")
    student_scientific_competitive_and_olympiad_movement_participant = Column("student_scientific_competitive_and_olympiad_movement_participant", Integer, nullable=False, default="-1")
    vocational_guidance_participant = Column("vocational_guidance_participant", Integer, nullable=False, default="-1")
    patriotic_projects_experience = Column("patriotic_projects_experience", Integer, nullable=False, default="-1")
    educational_activities_participation = Column("educational_activities_participation", Integer, nullable=False, default="-1")

    #page 6
    other_social_public_educational_work = Column("other_social_public_educational_work", Integer, nullable=False, default="-1")
    pedagogical_dynasty = Column("pedagogical_dynasty", Integer, nullable=False, default="-1")
    applications_and_characteristics_files = Column("applications_and_characteristics_files", Integer, nullable=False, default="-1")
    other_files = Column("other_files", Integer, nullable=False, default="-1")

    essay = Column("essay", Integer, nullable=False, default="-1")

    comment = Column("comment", Text)

    points = Column("points", Integer, nullable=False, default="0")