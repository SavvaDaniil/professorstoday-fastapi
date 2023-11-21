

class UserExpertFoundedTooMuchException(Exception):
    def __init__(self):
        super().__init__("founded_too_much")

class UserExpertNoChoosenNominationsException(Exception):
    def __init__(self):
        super().__init__("no_choosen_nominations")

class UsernameAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("username_already_exists")

class UserExpertNotFoundException(Exception):
    def __init__(self):
        super().__init__("User expert not found")

class UserNotFoundException(Exception):
    def __init__(self):
        super().__init__("User not found")

class UserProfileNotFilledException(Exception):
    def __init__(self):
        super().__init__("profile_not_filled")

class UserNotExpertException(Exception):
    def __init__(self):
        super().__init__("user_not_expert")

class UserNotExpertSetupedException(Exception):
    def __init__(self):
        super().__init__("user_expert_not_setuped")

class UserAlreadyWinnerException(Exception):
    def __init__(self):
        super().__init__("user_already_winner")


class UserPhotoFileTooLargeException(Exception):
    def __init__(self):
        super().__init__("User photo file too large")