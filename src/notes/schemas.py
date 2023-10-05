from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BoardBase(BaseModel):
    name: str


class BoardCreate(BoardBase):
    pass


class Board(BoardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BoardUpdate(BoardBase):
    pass


class BoardRetrieve(BaseModel):
    id: int


class BoardDelete(BaseModel):
    id: str


class NoteBase(BaseModel):
    text: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int | None = None
    views_count: int | None = None
    created_at: datetime
    updated_at: datetime


class NoteUpdate(NoteBase):
    pass


class NoteRetrieve(BaseModel):
    id: int


class NoteDelete(BaseModel):
    id: int


class LinkNoteToBoard(BaseModel):
    board_id: int
    note_id: int


class UnlinkNoteToBoard(BaseModel):
    board_id: int
    note_id: int
