import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"


class MediaCategory(str, enum.Enum):
    movie = "movie"
    education = "education"
    entertainment = "entertainment"
    book = "book"
    podcast = "podcast"
    article = "article"
    other = "other"


class MediaStatus(str, enum.Enum):
    unwatched = "unwatched"
    watching = "watching"
    completed = "completed"
    dropped = "dropped"
    on_hold = "on_hold"


class MediaPlatform(str, enum.Enum):
    youtube = "youtube"
    netflix = "netflix"
    prime_video = "prime_video"
    disney_plus = "disney_plus"
    instagram = "instagram"
    hotstar = "hotstar"
    other = "other"


class EducationTopic(str, enum.Enum):
    ai_ml = "ai_ml"
    computer_science = "computer_science"
    information_science = "information_science"
    web_dev = "web_dev"
    mathematics = "mathematics"
    science = "science"
    general = "general"


class TodoStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class DayOfWeek(str, enum.Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    media_items = relationship("MediaItem", back_populates="user", cascade="all, delete-orphan")
    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="user", cascade="all, delete-orphan")
    timetable_entries = relationship("TimetableEntry", back_populates="user", cascade="all, delete-orphan")
    calendar_days = relationship("CalendarDay", back_populates="user", cascade="all, delete-orphan")
    attendance_records = relationship("AttendanceRecord", back_populates="user", cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    color = Column(String(7), default="#6366F1")

    user = relationship("User", back_populates="tags")
    media_items = relationship("MediaItem", secondary="media_tags", back_populates="tags")


class MediaTag(Base):
    __tablename__ = "media_tags"

    media_item_id = Column(UUID(as_uuid=True), ForeignKey("media_items.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)


class MediaItem(Base):
    __tablename__ = "media_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    url = Column(Text, nullable=False)
    title = Column(String(500))
    description = Column(Text)
    thumbnail_url = Column(Text)
    category = Column(Enum(MediaCategory))
    status = Column(Enum(MediaStatus), default=MediaStatus.unwatched)
    platform = Column(Enum(MediaPlatform))
    channel_name = Column(String(200))
    duration = Column(Integer)
    priority_score = Column(Integer, default=5)
    notes = Column(Text)
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="media_items")
    education_metadata = relationship("EducationMetadata", back_populates="media_item", uselist=False, cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="media_tags", back_populates="media_items")


class EducationMetadata(Base):
    __tablename__ = "education_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    media_item_id = Column(UUID(as_uuid=True), ForeignKey("media_items.id", ondelete="CASCADE"), unique=True)
    topic = Column(Enum(EducationTopic))
    course_name = Column(String(200))
    instructor = Column(String(200))

    media_item = relationship("MediaItem", back_populates="education_metadata")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority_score = Column(Integer, default=5)
    status = Column(Enum(TodoStatus), default=TodoStatus.pending)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="todos")


class TimetableEntry(Base):
    __tablename__ = "timetable_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    subject = Column(String(200), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room = Column(String(100))

    user = relationship("User", back_populates="timetable_entries")


class CalendarDay(Base):
    __tablename__ = "calendar_days"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    is_working_day = Column(Boolean, default=True)
    notes = Column(String(200))

    user = relationship("User", back_populates="calendar_days")

    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='uq_calendar_user_date'),
    )


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    subject = Column(String(200), nullable=False)
    was_present = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="attendance_records")

    __table_args__ = (
        UniqueConstraint('user_id', 'date', 'subject', name='uq_attendance_user_date_subject'),
    )
