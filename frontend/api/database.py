from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Use SUPABASE_URL if available, otherwise default to SQLite (for local testing before deploying)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leads.db")

# Supabase PostgreSQL connection requires a slightly different engine config than SQLite
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Fix postgres:// to postgresql:// if needed
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String, unique=True, index=True)
    business_name = Column(String, index=True)
    category = Column(String)
    city = Column(String)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    phone = Column(String, nullable=True)
    whatsapp_link = Column(String, nullable=True)
    map_url = Column(String, nullable=True)
    address = Column(String, nullable=True)
    website = Column(String, nullable=True)
    email = Column(String, nullable=True)
    has_website = Column(Boolean, default=False)
    booking_detected = Column(Boolean, default=False)
    lead_score = Column(Integer, default=0)
    lead_grade = Column(String, default="🔴 Skip")  # 🔥 Hot, 🟢 Good, 🟡 Medium, 🔴 Skip
    recommended_pitch = Column(Text, nullable=True)
    status = Column(String, default="New") # New, Contacted, Won, Lost

Base.metadata.create_all(bind=engine)
