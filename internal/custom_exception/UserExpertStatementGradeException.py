

class UserExpertStatementGradeAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("already_exists")

class UserExpertStatementGradeNotFoundException(Exception):
    def __init__(self):
        super().__init__("UserExpertStatementGrade_not_found")
