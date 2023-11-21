

class UniversityNotFoundException(Exception):
    def __init__(self):
        super().__init__("University not found")