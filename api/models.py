"""SQLAlchemy ORM models for IT Training System."""

import os
from sqlalchemy import Column, Integer, String, Text, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)
    current_level = Column(String, nullable=True)
    manager_id = Column(Integer, nullable=True)


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    raw_transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    duration = Column(Integer, nullable=True)
    uploaded_by = Column(Integer, nullable=True)
    created_at = Column(String, nullable=True)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)


class VideoSkill(Base):
    __tablename__ = "video_skills"

    video_id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, primary_key=True)


class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, primary_key=True)
    proficiency_score = Column(Float, nullable=True)


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    questions_json = Column(Text, nullable=True)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, nullable=True)
    text = Column(Text, nullable=True)
    options_json = Column(Text, nullable=True)
    correct_index = Column(Integer, nullable=True)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    quiz_id = Column(Integer, nullable=True)
    score = Column(Float, nullable=True)
    completed_at = Column(String, nullable=True)


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(String, nullable=True)


class LearningPathItem(Base):
    __tablename__ = "learning_path_items"

    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(Integer, nullable=True)
    item_order = Column(Integer, nullable=True)
    item_type = Column(String, nullable=True)
    item_id = Column(Integer, nullable=True)
    completed = Column(Integer, default=0)


class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    event_type = Column(String, nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(String, nullable=True)
