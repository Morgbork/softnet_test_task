from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    text: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    views_count: int | None = None
    created_at: datetime
    updated_at: datetime


class NoteUpdate(NoteBase):
    pass


class LinkNoteToBoard(BaseModel):
    board_id: int
    note_id: int


class UnlinkNoteToBoard(BaseModel):
    board_id: int
    note_id: int


class BoardBase(BaseModel):
    name: str


class BoardCreate(BoardBase):
    pass


class Board(BoardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    notes: list[Note] = []
    created_at: datetime
    updated_at: datetime


class BoardUpdate(BoardBase):
    pass
