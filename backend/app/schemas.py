from datetime import date, datetime, time
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import (
    DayOfWeek,
    EducationTopic,
    MediaCategory,
    MediaPlatform,
    MediaStatus,
    TodoStatus,
    UserRole,
)


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: UUID
    role: UserRole
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TokenData(BaseModel):
    user_id: str
    username: str
    role: str


class TagBase(BaseModel):
    name: str = Field(..., max_length=50)
    color: str = Field(default="#6366F1", pattern=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, pattern=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")


class TagOut(TagBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class EducationMetadataBase(BaseModel):
    topic: Optional[EducationTopic] = None
    course_name: Optional[str] = None
    instructor: Optional[str] = None


class EducationMetadataUpdate(EducationMetadataBase):
    pass


class EducationMetadataOut(EducationMetadataBase):
    model_config = ConfigDict(from_attributes=True)


class MediaItemCreate(BaseModel):
    url: str
    priority_score: int = Field(default=5, ge=1, le=10)
    notes: Optional[str] = None


class MediaItemUpdate(BaseModel):
    status: Optional[MediaStatus] = None
    category: Optional[MediaCategory] = None
    notes: Optional[str] = None
    priority_score: Optional[int] = Field(None, ge=1, le=10)
    title: Optional[str] = None


class MediaItemListOut(BaseModel):
    id: UUID
    url: str
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category: Optional[MediaCategory] = None
    status: MediaStatus
    platform: Optional[MediaPlatform] = None
    channel_name: Optional[str] = None
    duration: Optional[int] = None
    priority_score: int
    notes: Optional[str] = None
    confidence: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    tags: List[TagOut] = []
    model_config = ConfigDict(from_attributes=True)


class MediaItemOut(MediaItemListOut):
    description: Optional[str] = None
    education_metadata: Optional[EducationMetadataOut] = None
    model_config = ConfigDict(from_attributes=True)


class LinkAnalysisResult(BaseModel):
    title: Optional[str] = None
    channel: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    platform: str
    category: str
    education_topic: Optional[str] = None
    tags: List[str] = []
    confidence: float


class TodoCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    priority_score: int = Field(default=5, ge=1, le=10)
    due_date: Optional[date] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    priority_score: Optional[int] = Field(None, ge=1, le=10)
    status: Optional[TodoStatus] = None
    due_date: Optional[date] = None


class TodoOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    priority_score: int
    status: TodoStatus
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class LeaderboardEntry(BaseModel):
    rank: int
    item_type: str
    id: UUID
    title: str
    priority_score: int
    status: str
    category: Optional[str] = None
    platform: Optional[str] = None
    thumbnail_url: Optional[str] = None
    due_date: Optional[date] = None


class TimetableEntryBase(BaseModel):
    day_of_week: DayOfWeek
    subject: str = Field(..., max_length=200)
    start_time: time
    end_time: time
    room: Optional[str] = Field(None, max_length=100)


class TimetableEntryUpdate(BaseModel):
    subject: Optional[str] = Field(None, max_length=200)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    room: Optional[str] = Field(None, max_length=100)


class TimetableEntryOut(TimetableEntryBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class AttendanceRecord(BaseModel):
    subject: str = Field(..., max_length=200)
    was_present: bool


class AttendanceCreate(BaseModel):
    date: date
    records: List[AttendanceRecord]


class AttendanceRecordOut(AttendanceRecord):
    id: UUID
    date: date
    model_config = ConfigDict(from_attributes=True)


class CalendarDayUpdate(BaseModel):
    is_working_day: bool
    notes: Optional[str] = Field(None, max_length=200)


class CalendarDayOut(BaseModel):
    id: UUID
    date: date
    is_working_day: bool
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class SubjectAttendanceOut(BaseModel):
    subject: str
    total: int
    attended: int
    percentage: float


class AttendanceStatsOut(BaseModel):
    overall_percentage: float
    total_working_days: int
    total_attended: int
    by_subject: List[SubjectAttendanceOut]


class DashboardStats(BaseModel):
    total: int
    by_category: Dict[str, int]
    by_status: Dict[str, int]
    by_topic: Dict[str, int]
