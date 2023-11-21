from datetime import datetime
import os, hashlib
from fastapi import HTTPException, UploadFile
from typing import Union, List
from datetime import datetime

from internal.Entities import Contest, User, Statement, Nomination, Region, UserExpertStatementGrade
from internal.facade.UserFacade import UserFacade
from internal.repository.UserExpertStatementGradeRepository import UserExpertStatementGradeRepository
from internal.repository.UserRepository import UserRepository
from internal.repository.StatementRepository import StatementRepository
from internal.repository.NominationRepository import NominationRepository
from internal.dto.UserExpertStatementGradeDTO import UserExpertStatementGradeEditDTO, UserExpertStatementGradeNewDTO
from internal.factory.UserExpertStatementGradeFactory import UserExpertStatementGradeFactory
from internal.factory.UserFactory import UserFactory
from internal.custom_exception.UserExpertStatementGradeException import UserExpertStatementGradeNotFoundException, UserExpertStatementGradeAlreadyExistsException
from internal.custom_exception.UserCustomException import UserNotFoundException, UserExpertNotFoundException
from internal.custom_exception.StatementCustomException import StatementNotFoundException
from internal.viewmodel.UserExpertStatementGradeViewModel import UserExpertStatementGradeEditViewModel
from internal.viewmodel.UserViewModel import UserMicroViewModel

class UserExpertStatementGradeFacade():

    def __init__(self) -> None:
        self.userExpertStatementGradeRepository: UserExpertStatementGradeRepository = UserExpertStatementGradeRepository()
        #self.statementRepository: StatementRepository = StatementRepository()

    def add(self, userExpertStatementGradeNewDTO: UserExpertStatementGradeNewDTO) -> None:
        userRepository: UserRepository = UserRepository()
        user: User = userRepository.find_by_id(id=userExpertStatementGradeNewDTO.user_expert_id)
        if user is None:
            raise UserNotFoundException()
        
        if not user.is_expert:
            raise UserExpertNotFoundException()
        
        statementRepository: StatementRepository = StatementRepository()
        statement: Statement = statementRepository.find_by_id(id=userExpertStatementGradeNewDTO.statement_id)

        if statement is None:
            raise StatementNotFoundException()
        
        userExpertStatementGradeAlreadyExists: UserExpertStatementGrade = self.userExpertStatementGradeRepository.find_by_user_expert_id_and_statement_id(
            user_expert_id=userExpertStatementGradeNewDTO.user_expert_id,
            statement_id=userExpertStatementGradeNewDTO.statement_id
        )

        if userExpertStatementGradeAlreadyExists is not None:
            raise UserExpertStatementGradeAlreadyExistsException()
        
        date_now: datetime = datetime.now()

        userExpertStatementGrade: UserExpertStatementGrade = UserExpertStatementGrade()
        userExpertStatementGrade.user_expert_id = user.id
        userExpertStatementGrade.statement_id = statement.id
        userExpertStatementGrade.points = 0
        userExpertStatementGrade.date_of_add = date_now
        userExpertStatementGrade.date_of_update = date_now
        self.userExpertStatementGradeRepository.add(obj=userExpertStatementGrade)

        userFacade: UserFacade = UserFacade()
        userFacade.send_mail_to_user_expert_about_new_user_expert_statement_grade(
            user=user,
            userExpertStatementGrade=userExpertStatementGrade
        )

    def set_points_to_all_appreciated(self) -> None:
        userExpertStatementGrades: List[UserExpertStatementGrade] = self.userExpertStatementGradeRepository.list_all_appreciated()
        for userExpertStatementGrade in userExpertStatementGrades:
            if userExpertStatementGrade.points != 0:
                continue
            #print("Set points to userExpertStatementGrade id: " + str(userExpertStatementGrade.id))
            userExpertStatementGrade.points = self.count_result_points(userExpertStatementGrade=userExpertStatementGrade)
            self.userExpertStatementGradeRepository.update(userExpertStatementGrade=userExpertStatementGrade)


    def count_result_points(self, userExpertStatementGrade: UserExpertStatementGrade) -> int:
        
        statementRepository: StatementRepository = StatementRepository()
        statement: Statement = statementRepository.find_by_id(id=userExpertStatementGrade.statement_id)
        if statement is None:
            raise StatementNotFoundException()
        
        nomination_id: int = statement.nomination_id
        points_amount: int = 0


        #page 2
        if userExpertStatementGrade.education > -1:
            points_amount += userExpertStatementGrade.education

        if userExpertStatementGrade.science_degree > -1:
            if nomination_id == 1:
                points_amount += userExpertStatementGrade.science_degree * 3
            else:
                points_amount += userExpertStatementGrade.science_degree
        
        if userExpertStatementGrade.academic_status > -1:
            if nomination_id == 1:
                points_amount += userExpertStatementGrade.academic_status * 3
            else:
                points_amount += userExpertStatementGrade.academic_status

        if userExpertStatementGrade.academic_rewards > -1:
            if nomination_id == 1:
                points_amount += userExpertStatementGrade.academic_rewards * 2
            elif nomination_id == 7:
                points_amount += userExpertStatementGrade.academic_rewards * 2
            else:
                points_amount += userExpertStatementGrade.academic_rewards

        ...

        return points_amount


    def list_edits_by_statement_id(self, statement_id: int) -> List[UserExpertStatementGradeEditViewModel]:
        userExpertStatementGradeEditViewModels: List[UserExpertStatementGradeEditViewModel] = []
        userExpertStatementGrades: List[UserExpertStatementGrade] = self.userExpertStatementGradeRepository.list_by_statement_id(statement_id=statement_id)
        if userExpertStatementGrades is None or len(userExpertStatementGrades) == 0:
            return userExpertStatementGradeEditViewModels
    
        userExpertStatementGradeFactory: UserExpertStatementGradeFactory = UserExpertStatementGradeFactory()

        userFactory: UserFactory = UserFactory()
        userExpertMicroViewModel: Union[UserMicroViewModel, None] = None
        userExpert: Union[User, None] = None

        for userExpertStatementGrade in userExpertStatementGrades:

            if userExpertStatementGrade.user_expert_id != 0 and userExpertStatementGrade.user_expert is not None:
                userExpert = userExpertStatementGrade.user_expert
                userExpertMicroViewModel = userFactory.create_micro(user=userExpert)
            else:
                userExpertMicroViewModel = None
            
            userExpertStatementGradeEditViewModels.append(
                userExpertStatementGradeFactory.create_edit(
                    userExpertStatementGrade=userExpertStatementGrade,
                    nominationMicroViewModel=None,
                    userProfileLiteViewModel=None,
                    userExpertMicroViewModel=userExpertMicroViewModel,
                    userStatementViewModel=None
                )
            )
        
        return userExpertStatementGradeEditViewModels


    def update(self, user_id: int, userExpertStatementGradeEditDTO: UserExpertStatementGradeEditDTO) -> None:
        userRepository: UserRepository = UserRepository()
        user: User = userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()

        userExpertStatementGrade: UserExpertStatementGrade = self.userExpertStatementGradeRepository.find_by_id(id=userExpertStatementGradeEditDTO.id)
        if userExpertStatementGrade is None or userExpertStatementGrade.user_expert_id != user_id:
            raise UserExpertStatementGradeNotFoundException()
        
        userExpertStatementGrade.education = self.__check_points_value(value=userExpertStatementGradeEditDTO.education)
        ...

        if userExpertStatementGrade.education != -1 \
		and userExpertStatementGrade.science_degree != -1 \
        ...:
            userExpertStatementGrade.is_appreciated = True
        else:
            userExpertStatementGrade.is_appreciated = False

        if userExpertStatementGrade.is_appreciated:
            userExpertStatementGrade.points = self.count_result_points(userExpertStatementGrade=userExpertStatementGrade)

        userExpertStatementGrade.date_of_update = datetime.now()
        self.userExpertStatementGradeRepository.update(userExpertStatementGrade=userExpertStatementGrade)

        statement: Statement = userExpertStatementGrade.statement
        if statement is not None:
            statementRepository: StatementRepository = StatementRepository()
            statement.is_appreciated = userExpertStatementGrade.is_appreciated

            statementRepository.update(statement=statement)


    def __check_points_value(self, value) -> int:
        return value if value >= -1 and value <= 5 else -1
    
        
        

