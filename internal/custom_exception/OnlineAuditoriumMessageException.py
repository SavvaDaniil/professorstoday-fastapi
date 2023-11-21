

class OnlineAuditoriumMessageAddFailedException(Exception):
    def __init__(self, message: str):
        super().__init__("Failed add OnlineAuditoriumMessage Exception: " + message)