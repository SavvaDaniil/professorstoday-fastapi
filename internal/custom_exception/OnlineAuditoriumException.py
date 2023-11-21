

class OnlineAuditoriumClosedException(Exception):
    def __init__(self):
        super().__init__("online_auditorium_closed")