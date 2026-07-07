import os
import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.timetable_ai import extract_timetable

router = APIRouter(prefix="/api/timetable", tags=["timetable"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

DAY_ORDER = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 7
}


@router.post("/upload", response_model=List[schemas.TimetableEntryOut])
async def upload_timetable(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Upload timetable image and extract data using AI."""
    # Save file
    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{file_ext}")
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    try:
        # Extract data
        entries = await extract_timetable(file_path)
        
        # Delete old entries
        db.query(models.TimetableEntry).filter(models.TimetableEntry.user_id == current_user.id).delete()
        
        # Save new entries
        db_entries = []
        for entry in entries:
            db_entry = models.TimetableEntry(
                user_id=current_user.id,
                day_of_week=models.DayOfWeek(entry["day_of_week"]),
                subject=entry["subject"],
                start_time=entry["start_time"],
                end_time=entry["end_time"],
                room=entry["room"]
            )
            db.add(db_entry)
            db_entries.append(db_entry)
            
        db.commit()
        for e in db_entries:
            db.refresh(e)
            
        return db_entries
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("", response_model=List[schemas.TimetableEntryOut])
def get_all_timetable_entries(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get all timetable entries for the user."""
    entries = db.query(models.TimetableEntry).filter(models.TimetableEntry.user_id == current_user.id).all()
    # Sort by day order then start time
    entries.sort(key=lambda x: (DAY_ORDER.get(x.day_of_week.value, 8), x.start_time))
    return entries


@router.get("/today", response_model=List[schemas.TimetableEntryOut])
def get_today_timetable(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get today's timetable entries."""
    today = datetime.now().strftime('%A').lower()
    entries = db.query(models.TimetableEntry).filter(
        models.TimetableEntry.user_id == current_user.id,
        models.TimetableEntry.day_of_week == today
    ).order_by(models.TimetableEntry.start_time).all()
    return entries


@router.get("/{day}", response_model=List[schemas.TimetableEntryOut])
def get_day_timetable(
    day: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get timetable entries for a specific day."""
    if day not in DAY_ORDER:
        raise HTTPException(status_code=400, detail="Invalid day of week")
        
    entries = db.query(models.TimetableEntry).filter(
        models.TimetableEntry.user_id == current_user.id,
        models.TimetableEntry.day_of_week == day
    ).order_by(models.TimetableEntry.start_time).all()
    return entries


@router.put("/{entry_id}", response_model=schemas.TimetableEntryOut)
def update_timetable_entry(
    entry_id: str,
    entry_in: schemas.TimetableEntryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update a timetable entry."""
    entry = db.query(models.TimetableEntry).filter(
        models.TimetableEntry.id == entry_id,
        models.TimetableEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
        
    update_data = entry_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(entry, key, value)
        
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_timetable_entry(
    entry_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete a timetable entry."""
    entry = db.query(models.TimetableEntry).filter(
        models.TimetableEntry.id == entry_id,
        models.TimetableEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
        
    db.delete(entry)
    db.commit()
    return None


@router.delete("")
def clear_timetable(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Clear all timetable entries."""
    db.query(models.TimetableEntry).filter(models.TimetableEntry.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Timetable cleared successfully"}
