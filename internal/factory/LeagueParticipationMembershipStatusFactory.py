
from internal.Entities import LeagueParticipationMembershipStatus
from internal.viewmodel.LeagueParticipationMembershipStatusViewModel import LeagueParticipationMembershipStatusMicroViewModel

class LeagueParticipationMembershipStatusFactory():

    def create_micro(self, leagueParticipationMembershipStatus: LeagueParticipationMembershipStatus) -> LeagueParticipationMembershipStatusMicroViewModel:
        return LeagueParticipationMembershipStatusMicroViewModel(
            id=leagueParticipationMembershipStatus.id,
            name=leagueParticipationMembershipStatus.name
        )