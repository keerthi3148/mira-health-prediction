import os
import datetime
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Define database URL (using SQLite in the local directory)
DATABASE_URL = "sqlite:///patients.db"

# Create the SQLAlchemy engine
# "check_same_thread": False is required for SQLite in multithreaded environments like Flask
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class for our models
Base = declarative_base()

class Patient(Base):
    """
    Patient database model storing demographic details, blood test metrics,
    and the AI-generated health prediction remarks.
    """
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    dob = Column(String, nullable=False)  # Stored in YYYY-MM-DD format
    email = Column(String, nullable=False)
    glucose = Column(Float, nullable=False)        # mg/dL
    haemoglobin = Column(Float, nullable=False)    # g/dL
    cholesterol = Column(Float, nullable=False)    # mg/dL
    remarks = Column(String, nullable=True)        # AI/ML Prediction remarks
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        """Helper to serialize model instance to a dictionary."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "dob": self.dob,
            "email": self.email,
            "glucose": self.glucose,
            "haemoglobin": self.haemoglobin,
            "cholesterol": self.cholesterol,
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

def init_db():
    """Initializes the database and creates all tables."""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    """Context manager to ensure database sessions are cleanly opened and closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
