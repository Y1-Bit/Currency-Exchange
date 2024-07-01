class User:
    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name

    @staticmethod
    def get_user(user_id: int) -> "User":
        return User(user_id, "User Name")
