

class LeagueParticipationMembershipStatusNotFoundException(Exception):
    def __init__(self):
        super().__init__("LeagueParticipationMembershipStatus not found")