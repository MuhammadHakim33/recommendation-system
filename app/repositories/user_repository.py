from sqlmodel import Session, select
from models.User import User
from configs.db import engine

class UserRepository:
    def get_all_users(self, limit: int = 100):
        """Get all users from MySQL"""
        try:
            with Session(engine) as session:
                statement = select(User).limit(limit)
                result = session.exec(statement)
                return result.all()
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []