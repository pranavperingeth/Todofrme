import calendar
from collections import defaultdict
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("", response_model=List[schemas.AttendanceRecordOut])
def record_attendance(
    attendance_in: schemas.AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Record or update attendance for a specific date."""
    records_out = []
    for record in attendance_in.records:
        existing = db.query(models.AttendanceRecord).filter(
            models.AttendanceRecord.user_id == current_user.id,
            models.AttendanceRecord.date == attendance_in.date,
            models.AttendanceRecord.subject == record.subject
        ).first()
        
        if existing:
            existing.was_present = record.was_present
            records_out.append(existing)
        else:
            new_record = models.AttendanceRecord(
                user_id=current_user.id,
                date=attendance_in.date,
                subject=record.subject,
                was_present=record.was_present
            )
            db.add(new_record)
            records_out.append(new_record)
            
    db.commit()
    for r in records_out:
        db.refresh(r)
        
    return records_out


@router.get("", response_model=List[schemas.AttendanceRecordOut])
def get_attendance(
    target_date: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get attendance records for a specific date."""
    return db.query(models.AttendanceRecord).filter(
        models.AttendanceRecord.user_id == current_user.id,
        models.AttendanceRecord.date == target_date
    ).all()


@router.get("/today")
def get_today_attendance_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get today's subjects and their attendance status."""
    today = datetime.now()
    today_date = today.date()
    today_name = today.strftime('%A').lower()
    
    # Check if today is marked as non-working
    cal_day = db.query(models.CalendarDay).filter(
        models.CalendarDay.user_id == current_user.id,
        models.CalendarDay.date == today_date
    ).first()
    
    if cal_day and not cal_day.is_working_day:
        return []
        
    timetable = db.query(models.TimetableEntry).filter(
        models.TimetableEntry.user_id == current_user.id,
        models.TimetableEntry.day_of_week == today_name
    ).all()
    
    # Get distinct subjects for today
    subjects = list(set([t.subject for t in timetable]))
    
    # Check existing attendance
    records = db.query(models.AttendanceRecord).filter(
        models.AttendanceRecord.user_id == current_user.id,
        models.AttendanceRecord.date == today_date
    ).all()
    record_map = {r.subject: r.was_present for r in records}
    
    result = []
    for subject in subjects:
        result.append({
            "subject": subject,
            "was_present": record_map.get(subject, None)
        })
        
    return result


@router.get("/stats", response_model=schemas.AttendanceStatsOut)
def get_attendance_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get per-subject and overall attendance statistics."""
    records = db.query(models.AttendanceRecord).filter(
        models.AttendanceRecord.user_id == current_user.id
    ).all()
    
    subject_stats = defaultdict(lambda: {'total': 0, 'attended': 0})
    for r in records:
        subject_stats[r.subject]['total'] += 1
        if r.was_present:
            subject_stats[r.subject]['attended'] += 1
            
    by_subject = []
    total_classes = 0
    total_attended = 0
    
    for subject, stats in subject_stats.items():
        total_classes += stats['total']
        total_attended += stats['attended']
        pct = (stats['attended'] / stats['total'] * 100) if stats['total'] > 0 else 0
        by_subject.append(schemas.SubjectAttendanceOut(
            subject=subject, 
            total=stats['total'], 
            attended=stats['attended'], 
            percentage=round(pct, 1)
        ))
        
    overall = (total_attended / total_classes * 100) if total_classes > 0 else 0
    
    # Calculate working days with recorded attendance
    working_days = len(set(r.date for r in records))
    
    return schemas.AttendanceStatsOut(
        overall_percentage=round(overall, 1),
        total_working_days=working_days,
        total_attended=total_attended,
        by_subject=by_subject
    )


@router.get("/subjects", response_model=List[str])
def get_subjects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get all unique subjects from timetable."""
    entries = db.query(models.TimetableEntry.subject).filter(
        models.TimetableEntry.user_id == current_user.id
    ).distinct().all()
    return [e[0] for e in entries]


@router.get("/calendar", response_model=List[schemas.CalendarDayOut])
def get_calendar(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get calendar data for a month, auto-creating defaults if needed."""
    _, num_days = calendar.monthrange(year, month)
    start_date = date(year, month, 1)
    end_date = date(year, month, num_days)
    
    existing = db.query(models.CalendarDay).filter(
        models.CalendarDay.user_id == current_user.id,
        models.CalendarDay.date >= start_date,
        models.CalendarDay.date <= end_date
    ).all()
    
    existing_map = {d.date: d for d in existing}
    
    result = []
    for day in range(1, num_days + 1):
        d = date(year, month, day)
        if d in existing_map:
            result.append(existing_map[d])
        else:
            # By default, weekends might be non-working, but let's assume all working 
            # unless user sets them. Actually, Saturday/Sunday usually non-working for some,
            # but let's default to True and let user toggle.
            result.append(models.CalendarDay(
                id=uuid.uuid4(), # temporary for schema
                user_id=current_user.id,
                date=d,
                is_working_day=True,
                notes=None
            ))
            
    return result


@router.put("/calendar/{date_str}", response_model=schemas.CalendarDayOut)
def update_calendar_day(
    date_str: date,
    update_data: schemas.CalendarDayUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Toggle working day status for a specific date."""
    cal_day = db.query(models.CalendarDay).filter(
        models.CalendarDay.user_id == current_user.id,
        models.CalendarDay.date == date_str
    ).first()
    
    if cal_day:
        cal_day.is_working_day = update_data.is_working_day
        cal_day.notes = update_data.notes
    else:
        cal_day = models.CalendarDay(
            user_id=current_user.id,
            date=date_str,
            is_working_day=update_data.is_working_day,
            notes=update_data.notes
        )
        db.add(cal_day)
        
    db.commit()
    db.refresh(cal_day)
    return cal_day
