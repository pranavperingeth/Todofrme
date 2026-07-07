from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.categorizer import analyze_url
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/media", tags=["media"])


@router.post("/analyze", response_model=schemas.LinkAnalysisResult)
async def preview_media(
    url: str = Query(..., description="URL to analyze"),
    current_user: models.User = Depends(get_current_user),
):
    """Analyze a URL without saving it."""
    result = await analyze_url(url)
    return result


@router.post("", response_model=schemas.MediaItemOut, status_code=status.HTTP_201_CREATED)
async def create_media_item(
    item_in: schemas.MediaItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Add a new media item with auto-categorization."""
    # Run analysis
    analysis = await analyze_url(item_in.url)
    
    db_item = models.MediaItem(
        user_id=current_user.id,
        url=item_in.url,
        title=analysis["title"],
        description=analysis["description"],
        thumbnail_url=analysis["thumbnail"],
        category=models.MediaCategory(analysis["category"]),
        platform=models.MediaPlatform(analysis["platform"]),
        channel_name=analysis["channel"],
        duration=analysis["duration"],
        priority_score=item_in.priority_score,
        notes=item_in.notes,
        confidence=analysis["confidence"],
    )
    db.add(db_item)
    db.flush() # flush to get db_item.id
    
    if analysis["category"] == models.MediaCategory.education.value and analysis.get("education_topic"):
        db_edu = models.EducationMetadata(
            media_item_id=db_item.id,
            topic=models.EducationTopic(analysis["education_topic"]),
            instructor=analysis["channel"]
        )
        db.add(db_edu)
        
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("", response_model=List[schemas.MediaItemListOut])
def list_media(
    category: Optional[models.MediaCategory] = None,
    status_filter: Optional[models.MediaStatus] = Query(None, alias="status"),
    platform: Optional[models.MediaPlatform] = None,
    topic: Optional[models.EducationTopic] = None,
    search: Optional[str] = None,
    sort_by: str = Query("priority_score", pattern="^(priority_score|created_at)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """List media items with filtering and pagination."""
    query = db.query(models.MediaItem).filter(models.MediaItem.user_id == current_user.id)
    
    if category:
        query = query.filter(models.MediaItem.category == category)
    if status_filter:
        query = query.filter(models.MediaItem.status == status_filter)
    if platform:
        query = query.filter(models.MediaItem.platform == platform)
    if search:
        query = query.filter(models.MediaItem.title.ilike(f"%{search}%"))
        
    if topic:
        query = query.join(models.EducationMetadata).filter(
            models.EducationMetadata.topic == topic
        )
        
    if sort_by == "priority_score":
        query = query.order_by(models.MediaItem.priority_score.desc(), models.MediaItem.created_at.desc())
    else:
        query = query.order_by(models.MediaItem.created_at.desc())
        
    offset = (page - 1) * limit
    items = query.options(joinedload(models.MediaItem.tags)).offset(offset).limit(limit).all()
    return items


@router.get("/stats", response_model=schemas.DashboardStats)
def get_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get dashboard statistics for the user."""
    items = db.query(models.MediaItem).filter(models.MediaItem.user_id == current_user.id).all()
    
    total = len(items)
    by_category = {}
    by_status = {}
    by_topic = {}
    
    for item in items:
        # Category
        cat = item.category.value if item.category else "unknown"
        by_category[cat] = by_category.get(cat, 0) + 1
        
        # Status
        stat = item.status.value if item.status else "unknown"
        by_status[stat] = by_status.get(stat, 0) + 1
        
        # Topic
        if item.category == models.MediaCategory.education and item.education_metadata and item.education_metadata.topic:
            top = item.education_metadata.topic.value
            by_topic[top] = by_topic.get(top, 0) + 1
            
    return {
        "total": total,
        "by_category": by_category,
        "by_status": by_status,
        "by_topic": by_topic
    }


@router.get("/{media_id}", response_model=schemas.MediaItemOut)
def get_media_item(
    media_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get a specific media item by ID."""
    item = db.query(models.MediaItem).filter(
        models.MediaItem.id == media_id,
        models.MediaItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")
    return item


@router.put("/{media_id}", response_model=schemas.MediaItemOut)
def update_media_item(
    media_id: str,
    item_in: schemas.MediaItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update a media item."""
    item = db.query(models.MediaItem).filter(
        models.MediaItem.id == media_id,
        models.MediaItem.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")
        
    update_data = item_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(item, key, value)
        
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media_item(
    media_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete a media item."""
    item = db.query(models.MediaItem).filter(
        models.MediaItem.id == media_id,
        models.MediaItem.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")
        
    db.delete(item)
    db.commit()
    return None
