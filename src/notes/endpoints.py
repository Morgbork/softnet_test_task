from collections.abc import AsyncGenerator
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session
from src.notes import schemas
from src.notes.models import Board, Note

note_router = APIRouter()
board_router = APIRouter()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@note_router.post("", response_model=schemas.Note, status_code=201)
async def create_new_note(
    new_note: schemas.NoteCreate,
    session: AsyncSession = Depends(get_session),
):
    """Creates new note."""

    note = Note(text=new_note.text)

    session.add(note)
    await session.commit()

    return note


@note_router.get("/{note_id}", response_model=schemas.Note, status_code=200)
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


@note_router.patch("/{note_id}", response_model=schemas.Note, status_code=200)
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


@note_router.delete("/{note_id}", status_code=204)
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


@board_router.post("", response_model=schemas.Board, status_code=201)
async def create_new_board(
    new_board: schemas.BoardCreate,
    session: AsyncSession = Depends(get_session),
):
    """Creates new board."""

    board = Board(name=new_board.name)

    session.add(board)
    await session.commit()
    await session.refresh(board, ["notes"])
    return board


@board_router.get("/{board_id}", response_model=schemas.Board, status_code=200)
async def get_board(
    board_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Returns board by id."""

    board = await session.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A board with this id does not exist."}],
        )
    await session.refresh(board, ["notes"])
    return board


@board_router.patch("/{board_id}", response_model=schemas.Board, status_code=200)
async def update_board(
    board_id: int,
    new_data: schemas.BoardUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Updates board."""

    board = await session.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A board with this id does not exist."}],
        )
    for field in new_data.model_fields:
        setattr(board, field, getattr(new_data, field))
    await session.commit()
    await session.refresh(board, ["notes"])
    return board


@board_router.delete("/{board_id}", status_code=204)
async def delete_board(
    board_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Deletes board."""

    board = await session.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A board with this id does not exist."}],
        )
    await session.delete(board)
    await session.commit()


@board_router.post(
    "/{board_id}/link-note/{note_id}", response_model=schemas.Board, status_code=201
)
async def link_note_to_board(
    board_id: int,
    note_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Links a note to a board."""

    board = await session.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A board with this id does not exist."}],
        )

    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A note with this id does not exist."}],
        )

    note.board_id = board_id
    board.updated_at = datetime.now()
    await session.commit()
    await session.refresh(board, ["notes"])
    return board


@board_router.post(
    "/{board_id}/unlink-note/{note_id}", response_model=schemas.Board, status_code=201
)
async def unlink_note_from_board(
    board_id: int,
    note_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Unlinks a note from a board."""

    board = await session.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A board with this id does not exist."}],
        )

    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A note with this id does not exist."}],
        )

    note.board_id = None
    board.updated_at = datetime.now()
    await session.commit()
    await session.refresh(board, ["notes"])
    return board
