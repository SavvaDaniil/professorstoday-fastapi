from typing import List

from internal.Entities import LeagueParticipationMembershipStatus
from internal.repository.LeagueParticipationMembershipStatusRepository import LeagueParticipationMembershipStatusRepository
from internal.viewmodel.LeagueParticipationMembershipStatusViewModel import LeagueParticipationMembershipStatusMicroViewModel
from internal.factory.LeagueParticipationMembershipStatusFactory import LeagueParticipationMembershipStatusFactory

class LeagueParticipationMembershipStatusFacade():

    def __init__(self) -> None:
        self.leagueParticipationMembershipStatusRepository: LeagueParticipationMembershipStatusRepository = LeagueParticipationMembershipStatusRepository()
        self.leagueParticipationMembershipStatusFactory: LeagueParticipationMembershipStatusFactory = LeagueParticipationMembershipStatusFactory()

    def list_micro_for_user(self) -> List[LeagueParticipationMembershipStatusMicroViewModel]:
        leagueParticipationMembershipStatusMicroViewModels: List[LeagueParticipationMembershipStatusMicroViewModel] = []
        leagueParticipationMembershipStatuses: List[LeagueParticipationMembershipStatus] = self.leagueParticipationMembershipStatusRepository.list_all_active()

        for leagueParticipationMembershipStatus in leagueParticipationMembershipStatuses:
            leagueParticipationMembershipStatusMicroViewModels.append(
                self.leagueParticipationMembershipStatusFactory.create_micro(leagueParticipationMembershipStatus=leagueParticipationMembershipStatus)
            )
        
        return leagueParticipationMembershipStatusMicroViewModels