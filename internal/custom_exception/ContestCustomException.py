

class ContestNotFoundException(Exception):
    def __init__(self):
        super().__init__("Contest not found")