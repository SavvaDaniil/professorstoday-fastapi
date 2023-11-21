from typing import Union

from internal.Entities import User
from internal.factory.RegionFactory import RegionFactory
from internal.viewmodel.UserViewModel import UserPreviewViewModel, UserMicroViewModel, UserProfileLiteViewModel
from internal.viewmodel.RegionViewModel import RegionMicroViewModel
from internal.viewmodel.LeagueParticipationMembershipStatusViewModel import LeagueParticipationMembershipStatusMicroViewModel
from internal.factory.LeagueParticipationMembershipStatusFactory import LeagueParticipationMembershipStatusFactory

class UserFactory:

    def create_profile_lite(self, user: User) -> UserProfileLiteViewModel:

        return UserProfileLiteViewModel(
            id=user.id,
            username=user.username,
            secondname=user.secondname,
            firstname=user.firstname,
            patronymic=user.patronymic,
            
            gender=user.gender,

            birthday = (user.birthday.strftime("%Y-%m-%d") if user.birthday is not None else None),
            ...
        )
    
    def create_micro(self, user: User) -> UserMicroViewModel:
        return UserMicroViewModel(
            id=user.id,
            username=user.username,
            secondname=user.secondname,
            firstname=user.firstname
        )

    def create_preview(self, user: User) -> UserPreviewViewModel:

        regionMicroViewModel: Union[RegionMicroViewModel, None] = None
        if user.region_id != 0 and user.region is not None:
            regionFactory: RegionFactory = RegionFactory()
            regionMicroViewModel = regionFactory.create_micro(region=user.region)

        leagueParticipationMembershipStatusMicroViewModel: Union[LeagueParticipationMembershipStatusMicroViewModel, None] = None
        if user.league_participation_membership_status_id !=0 and user.league_participation_membership_status is not None:
            leagueParticipationMembershipStatusFactory: LeagueParticipationMembershipStatusFactory = LeagueParticipationMembershipStatusFactory()
            leagueParticipationMembershipStatusMicroViewModel = leagueParticipationMembershipStatusFactory.create_micro(leagueParticipationMembershipStatus=user.league_participation_membership_status)
        
        return UserPreviewViewModel(
            id=user.id,
            username=user.username,
            secondname=user.secondname,
            ...
        )
