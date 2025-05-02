
from os import getenv

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, SQLModel

load_dotenv()

DATABASE_URL = (
    f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
    f"@{getenv('POSTGRES_HOST', 'db')}:{getenv('POSTGRES_PORT', '5432')}/"
    f"{getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL, future=True, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
