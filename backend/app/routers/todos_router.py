from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.post("", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_in: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create a new to-do."""
    db_todo = models.Todo(
        user_id=current_user.id,
        title=todo_in.title,
        description=todo_in.description,
        priority_score=todo_in.priority_score,
        due_date=todo_in.due_date,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("", response_model=List[schemas.TodoOut])
def list_todos(
    status_filter: Optional[models.TodoStatus] = Query(None, alias="status"),
    sort_by: str = Query("priority_score", pattern="^(priority_score|created_at|due_date)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """List to-dos for current user."""
    query = db.query(models.Todo).filter(models.Todo.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(models.Todo.status == status_filter)
        
    if sort_by == "priority_score":
        query = query.order_by(models.Todo.priority_score.desc(), models.Todo.created_at.desc())
    elif sort_by == "due_date":
        query = query.order_by(models.Todo.due_date.asc())
    else:
        query = query.order_by(models.Todo.created_at.desc())
        
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()


@router.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(
    type: str = Query("all", pattern="^(all|todo|media)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """UNIFIED leaderboard: combine todos + media items."""
    entries = []
    
    if type in ('all', 'todo'):
        todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
        for t in todos:
            entries.append({
                'item_type': 'todo', 
                'id': t.id, 
                'title': t.title,
                'priority_score': t.priority_score, 
                'status': t.status.value,
                'category': None, 
                'platform': None, 
                'thumbnail_url': None,
                'due_date': t.due_date,
            })
            
    if type in ('all', 'media'):
        media = db.query(models.MediaItem).filter(models.MediaItem.user_id == current_user.id).all()
        for m in media:
            entries.append({
                'item_type': 'media', 
                'id': m.id, 
                'title': m.title,
                'priority_score': m.priority_score, 
                'status': m.status.value,
                'category': m.category.value if m.category else None,
                'platform': m.platform.value if m.platform else None,
                'thumbnail_url': m.thumbnail_url, 
                'due_date': None,
            })

    # Sort by priority desc, then by created_at (implicitly kept order before sorting if equal, but python sort is stable)
    # We sort by priority_score descending
    entries.sort(key=lambda x: x['priority_score'], reverse=True)
    
    for i, entry in enumerate(entries, 1):
        entry['rank'] = i
        
    return entries


@router.get("/{todo_id}", response_model=schemas.TodoOut)
def get_todo(
    todo_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get single to-do."""
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == current_user.id
    ).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-do not found")
    return todo


@router.put("/{todo_id}", response_model=schemas.TodoOut)
def update_todo(
    todo_id: str,
    todo_in: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update to-do."""
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="To-do not found")
        
    update_data = todo_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
        
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete to-do."""
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="To-do not found")
        
    db.delete(todo)
    db.commit()
    return None
