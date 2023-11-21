
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import LeagueParticipationMembershipStatus
from typing import List, Union

class LeagueParticipationMembershipStatusRepository:

    def find_by_id(self, id: int) -> LeagueParticipationMembershipStatus:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(LeagueParticipationMembershipStatus).filter(LeagueParticipationMembershipStatus.id == id).order_by(LeagueParticipationMembershipStatus.id).first()
        finally:
            session.close()
            
        return obj

    def list_all(self) -> List[LeagueParticipationMembershipStatus]:
        objs: List[LeagueParticipationMembershipStatus] = []
        ...
        return objs
    

    def list_all_active(self) -> List[LeagueParticipationMembershipStatus]:
        objs: List[LeagueParticipationMembershipStatus] = []
        ...
        return objs