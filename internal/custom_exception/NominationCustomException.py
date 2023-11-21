

class NominationNotFoundException(Exception):
    def __init__(self):
        super().__init__("Nomination not found")