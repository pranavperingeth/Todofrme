from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import delete

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["tags"])


@router.post("/tags", response_model=schemas.TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_in: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create a new tag."""
    # Check if tag with same name already exists for this user
    existing = db.query(models.Tag).filter(
        models.Tag.user_id == current_user.id,
        models.Tag.name == tag_in.name
    ).first()
    
    if existing:
        return existing
        
    db_tag = models.Tag(
        user_id=current_user.id,
        name=tag_in.name,
        color=tag_in.color
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.get("/tags", response_model=List[schemas.TagOut])
def list_tags(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """List all tags for the user."""
    return db.query(models.Tag).filter(models.Tag.user_id == current_user.id).all()


@router.put("/tags/{tag_id}", response_model=schemas.TagOut)
def update_tag(
    tag_id: str,
    tag_in: schemas.TagUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update a tag."""
    tag = db.query(models.Tag).filter(
        models.Tag.id == tag_id,
        models.Tag.user_id == current_user.id
    ).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
        
    update_data = tag_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)
        
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete a tag."""
    tag = db.query(models.Tag).filter(
        models.Tag.id == tag_id,
        models.Tag.user_id == current_user.id
    ).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
        
    db.delete(tag)
    db.commit()
    return None


@router.post("/media/{media_id}/tags/{tag_id}")
def add_tag_to_media(
    media_id: str,
    tag_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Attach a tag to a media item."""
    # Check media ownership
    media = db.query(models.MediaItem).filter(
        models.MediaItem.id == media_id,
        models.MediaItem.user_id == current_user.id
    ).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media item not found")
        
    # Check tag ownership
    tag = db.query(models.Tag).filter(
        models.Tag.id == tag_id,
        models.Tag.user_id == current_user.id
    ).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
        
    # Check if already attached
    existing = db.query(models.MediaTag).filter(
        models.MediaTag.media_item_id == media_id,
        models.MediaTag.tag_id == tag_id
    ).first()
    
    if not existing:
        db_media_tag = models.MediaTag(media_item_id=media_id, tag_id=tag_id)
        db.add(db_media_tag)
        db.commit()
        
    return {"message": "Tag attached successfully"}


@router.delete("/media/{media_id}/tags/{tag_id}")
def remove_tag_from_media(
    media_id: str,
    tag_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Remove a tag from a media item."""
    stmt = delete(models.MediaTag).where(
        models.MediaTag.media_item_id == media_id,
        models.MediaTag.tag_id == tag_id
    )
    db.execute(stmt)
    db.commit()
    return {"message": "Tag removed successfully"}
