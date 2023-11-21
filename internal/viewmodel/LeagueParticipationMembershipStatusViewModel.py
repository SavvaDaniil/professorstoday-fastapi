from pydantic import BaseModel
from typing import Union

class LeagueParticipationMembershipStatusMicroViewModel(BaseModel):
    id: int
    name: Union[str, None]