import os

from typing import Union, List

from internal.Entities import Statement, User, UserExpertStatementGrade
from internal.repository.UserExpertStatementGradeRepository import UserExpertStatementGradeRepository
from internal.factory.UserFactory import UserFactory
from internal.factory.NominationFactory import NominationFactory
from internal.util.StatementUtil import StatementUtil
from internal.viewmodel.StatementViewModel import StatementPreviewViewModel
from internal.viewmodel.UserViewModel import UserMicroViewModel
from internal.viewmodel.ContestViewModel import ContestMicroViewModel
from internal.viewmodel.NominationViewModel import NominationMicroViewModel

class StatementFactory:

    def __init__(self) -> None:
        self.userExpertStatementGradeRepository: UserExpertStatementGradeRepository = UserExpertStatementGradeRepository()
        self.userFactory: UserFactory = UserFactory()
        self.nominationFactory: NominationFactory = NominationFactory()

    def create_preview(self, statement: Statement) -> StatementPreviewViewModel:
        
        userMicroViewModel: Union[UserMicroViewModel, None] = None
        if statement.user_id != 0 and statement.user is not None:
            userMicroViewModel = self.userFactory.create_micro(user=statement.user)

        nominationMicroViewModel: Union[NominationMicroViewModel, None] = None
        if statement.nomination_id != 0 and statement.nomination is not None:
            nominationMicroViewModel = self.nominationFactory.create_micro(nomination=statement.nomination)
        
        user_expert_statement_number: int = 0
        user_expert_statement_appreciated_number: int = 0

        #if statement.status == 1:
        userExpertStatementGrades: List[UserExpertStatementGrade] = self.userExpertStatementGradeRepository.list_by_statement_id(statement_id=statement.id)
        if userExpertStatementGrades is not None and len(userExpertStatementGrades) > 0:
            for userExpertStatementGrade in userExpertStatementGrades:
                user_expert_statement_number += 1
                if userExpertStatementGrade.is_appreciated:
                    user_expert_statement_appreciated_number += 1
        
        return StatementPreviewViewModel(
            id=statement.id,
            userMicroViewModel=userMicroViewModel,
            #contestMicroViewModel: Union[ContestMicroViewModel, None] = None
            status=statement.status,
            photo_file_src=StatementUtil.get_statement_file_src(statement_id=statement.id),
            ...
        )