from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import User, Note, NoteStatus as NoteStatusEnum
from app.schemas import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse, NoteStatus
from app.auth import get_current_user

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new note for the current user."""
    db_note = Note(
        title=note_data.title,
        description=note_data.description,
        status=NoteStatusEnum(note_data.status.value),
        user_id=current_user.id,
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return db_note


@router.get("", response_model=NoteListResponse)
def list_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[NoteStatus] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List notes for the current user with optional filtering by status."""
    query = db.query(Note).filter(Note.user_id == current_user.id)
    
    # Filter by status if provided
    if status:
        query = query.filter(Note.status == NoteStatusEnum(status.value))
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    notes = query.offset(skip).limit(limit).all()
    
    return {
        "items": notes,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific note by ID."""
    note = db.query(Note).filter(
        (Note.id == note_id) & (Note.user_id == current_user.id)
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a specific note."""
    note = db.query(Note).filter(
        (Note.id == note_id) & (Note.user_id == current_user.id)
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    
    # Update fields if provided
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.description is not None:
        note.description = note_data.description
    if note_data.status is not None:
        note.status = NoteStatusEnum(note_data.status.value)
    
    db.commit()
    db.refresh(note)
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a specific note."""
    note = db.query(Note).filter(
        (Note.id == note_id) & (Note.user_id == current_user.id)
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    
    db.delete(note)
    db.commit()
