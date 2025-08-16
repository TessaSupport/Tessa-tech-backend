from sqlalchemy import create_engine
from .baseClass import Base
from sqlalchemy.orm import sessionmaker
from utils.config import settings

DATABASE_URL = settings.DATABASE_URL

# Make database configuration environment-aware
if "sqlite" in DATABASE_URL.lower():
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"},
        pool_size=10,
        max_overflow=20
    )

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)