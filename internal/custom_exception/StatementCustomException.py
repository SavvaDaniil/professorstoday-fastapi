

class StatementNotFoundException(Exception):
    def __init__(self):
        super().__init__("Statement not found")