
from typing import List

from internal.Entities import Contest, User, Statement
from internal.repository.ContestRepository import ContestRepository
from internal.repository.UserRepository import UserRepository
from internal.repository.StatementRepository import StatementRepository
from internal.custom_exception.UserCustomException import UserNotFoundException
from internal.viewmodel.ContestViewModel import ContestUserStatementViewModel
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus

class ContestFacade:

    def __init__(self) -> None:
        self.userRepository: UserRepository = UserRepository()
        self.contestRepository: ContestRepository = ContestRepository()
        self.statementRepository: StatementRepository = StatementRepository()

    def list_with_user_statement_for_user(self, user_id: int) -> JsonAnswerStatus:

        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        if user.username is None or user.username == "" \
            ...:
            return JsonAnswerStatus(status="error", errors="profile_not_filled")
        
        if user.league_participation_membership_status_id > 1 and user.league_participation_membership_status_id < 7:
            return JsonAnswerStatus(status="error", errors="user_already_winner")
        
        if user.is_expert:
            return JsonAnswerStatus(status="error", errors="user_already_winner")
        
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
        jsonAnswerStatus.contestUserStatementViewModels = self.list_with_user_statement(user=user)
        return jsonAnswerStatus

    def list_with_user_statement(self, user: User) -> List[ContestUserStatementViewModel]:
        
        if user is None:
            raise UserNotFoundException()

        contestUserStatementViewModels: List[ContestUserStatementViewModel] = []
        contests: List[Contest] = self.contestRepository.list_all_visible()
        statements: List[Statement] = self.statementRepository.list_by_user_id(user_id=user.id)
        user_statement_is_start: bool = False
        user_statement_is_sent: bool = False
        is_active: bool = False

        for contest in contests:
            user_statement_is_start = False
            user_statement_is_sent = False
            is_active: bool = False
            for statement in statements:
                ...

            contestUserStatementViewModels.append(
                ContestUserStatementViewModel(
                    id=contest.id,
                    name=contest.name,
                    description=contest.description,
                    is_visible=(contest.is_visible == 1),
                    is_active=is_active,
                    is_blocked_statement_edit=contest.is_blocked_statement_edit,

                    user_statement_is_start=user_statement_is_start,
                    user_statement_is_sent=user_statement_is_sent,
                )
            )

        return contestUserStatementViewModels
