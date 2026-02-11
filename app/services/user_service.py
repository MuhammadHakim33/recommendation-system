from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_all_users(self, limit: int = 100):
        result = self.user_repo.get_all_users(limit)
        
        if not result:
            raise ValueError("No users found")

        return result