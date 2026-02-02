from configs.db import engine
from sqlmodel import Session, select
from models.UserHistory import UserHistory

def get_user_reading_history(user_id: int):
    with Session(engine) as session:
        statement = select(UserHistory).where(UserHistory.user_id == user_id)
        result = session.exec(statement)
        return result.all()