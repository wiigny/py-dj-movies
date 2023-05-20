class UniqueUserNameOrEmail(Exception):
    def __init__(self, message: dict) -> None:
        self.message = message
