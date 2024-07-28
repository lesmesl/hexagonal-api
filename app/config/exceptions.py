# User Exceptions
class UserAlreadyExistsException(Exception):
    def __init__(self, message="Email or Username already registered"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsException(Exception):
    def __init__(self, message="Incorrect username or password"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenException(Exception):
    def __init__(self, message="Could not validate credentials"):
        self.message = message
        super().__init__(self.message)


class DatabaseException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
