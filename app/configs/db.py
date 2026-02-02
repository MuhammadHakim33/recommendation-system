from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_ROOT_PASSWORD")
db_name = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create database connection
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# # Create database and tables if not exists
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# # Get session for dependency injection
# def get_session():
#     with Session(engine) as session:
#         yield session