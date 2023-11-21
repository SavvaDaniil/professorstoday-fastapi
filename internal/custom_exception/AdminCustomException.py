

class AdminNotFoundException(Exception):
    def __init__(self):
        super().__init__("Admin not found")

class AdminLoginFailedException(Exception):
    def __init__(self):
        super().__init__("wrong")
