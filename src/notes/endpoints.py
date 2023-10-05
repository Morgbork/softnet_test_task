from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session
from src.notes import schemas
from src.notes.models import Note

router = APIRouter()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@router.post("/note/", response_model=schemas.Note, status_code=201)
async def create_new_note(
    new_note: schemas.NoteCreate,
    session: AsyncSession = Depends(get_session),
):
    """Creates new note."""

    note = Note(text=new_note.text)

    session.add(note)
    await session.commit()

    return note


@router.get("/note/{note_id}", response_model=schemas.Note, status_code=200)
async def get_note(
    note_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Returns note by id."""

    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A note with this id does not exist."}],
        )
    note.views_count += 1
    await session.commit()

    return note


@router.patch("/note/{note_id}", response_model=schemas.Note, status_code=200)
async def update_note(
    note_id: int,
    new_data: schemas.NoteUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Updates note."""

    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A note with this id does not exist."}],
        )
    for field in new_data.model_fields:
        setattr(note, field, getattr(new_data, field))
    await session.commit()

    return note


@router.delete("/note/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Deletes note."""

    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A note with this id does not exist."}],
        )
    await session.delete(note)
    await session.commit()
