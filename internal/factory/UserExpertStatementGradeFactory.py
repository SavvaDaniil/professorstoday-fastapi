
from typing import List, Union

from internal.Entities import User, Statement, UserExpertStatementGrade, Nomination
from internal.repository.UserRepository import UserRepository
from internal.viewmodel.UserExpertStatementGradeViewModel import UserExpertStatementGradePreviewViewModel, UserExpertStatementGradeEditViewModel
from internal.viewmodel.NominationViewModel import NominationMicroViewModel
from internal.viewmodel.UserViewModel import UserMicroViewModel, UserProfileLiteViewModel
from internal.viewmodel.StatementViewModel import UserStatementViewModel
from internal.factory.UserFactory import UserFactory
from internal.factory.NominationFactory import NominationFactory

class UserExpertStatementGradeFactory():

    def create_edit(
            self, 
            userExpertStatementGrade: UserExpertStatementGrade, 
            nominationMicroViewModel: Union[NominationMicroViewModel, None] = None,
            userProfileLiteViewModel: Union[UserProfileLiteViewModel, None] = None,
            userExpertMicroViewModel: Union[UserMicroViewModel, None] = None,
            userStatementViewModel: Union[UserStatementViewModel, None] = None, 
    ) -> UserExpertStatementGradeEditViewModel:
        
        return UserExpertStatementGradeEditViewModel(
            id=userExpertStatementGrade.id,
            nominationMicroViewModel=nominationMicroViewModel,
            userProfileLiteViewModel=userProfileLiteViewModel,
            userExpertMicroViewModel=userExpertMicroViewModel,
            userStatementViewModel=userStatementViewModel,
            is_appreciated=userExpertStatementGrade.is_appreciated,

            #page 2
            education = userExpertStatementGrade.education,
            ...
        )





    def create_preview(self, userExpertStatementGrade: UserExpertStatementGrade) -> UserExpertStatementGradePreviewViewModel:

        statement_id: int = 0
        nominationMicroViewModel: Union[NominationMicroViewModel, None] = None
        userMicroViewModel: Union[UserMicroViewModel, None] = None

        if userExpertStatementGrade.statement is not None:
            statement: Statement = userExpertStatementGrade.statement
            statement_id = statement.id

            if statement.nomination is not None:
                nominationMicroViewModel = NominationMicroViewModel(
                    id=statement.nomination.id,
                    name=statement.nomination.name
                )

            if statement.user is not None:
                userFactory: UserFactory = UserFactory()
                userMicroViewModel = userFactory.create_micro(user=statement.user)

        return UserExpertStatementGradePreviewViewModel(
            id=userExpertStatementGrade.id,
            statement_id=statement_id,
            ...
        )