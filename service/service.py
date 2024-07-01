from typing import Any

from model.model import User


class UserService:
    @staticmethod
    def get_user_details(user_id) -> dict[str, Any]:
        user = User.get_user(user_id)
        return {"id": user.user_id, "name": user.name}
