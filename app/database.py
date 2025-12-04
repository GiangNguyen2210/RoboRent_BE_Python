from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import scoped_session
from app.models.models import Base

# =======================================
# DATABASE URL
# =======================================
DATABASE_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/RoboRent_BE"

# =======================================
# SQLALCHEMY ENGINE
# =======================================
engine = create_engine(
    DATABASE_URL,
    echo=False,          # Set True for debugging
    future=True
)

# =======================================
# SESSION FACTORY
# =======================================
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
    )
)

# =======================================
# Dependency for FastAPI
# =======================================
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =======================================
# Initialize DB if needed
# =======================================
def init_db():
    Base.metadata.create_all(bind=engine)
