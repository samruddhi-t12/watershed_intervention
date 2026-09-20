from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../data/sqlite/demo_db.sqlite")

# Ensure directory exists if it's a local sqlite path
db_path = DATABASE_URL.replace("sqlite:///", "")
if db_path.startswith("../"):
    db_path = os.path.join(os.path.dirname(__file__), db_path)
os.makedirs(os.path.dirname(db_path), exist_ok=True)

engine = create_engine(
    f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
