class DuplicateEmail(Exception):
    """Exception class intended to be thrown when a duplicate email is detected for a new member"""
    def __init__(self, message, email):
        super().__init__(message)
        self.email = email


