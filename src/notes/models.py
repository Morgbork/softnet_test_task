from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimeStampMixin(object):
    created_at = mapped_column(DateTime, default=datetime.now(), sort_order=999)
    updated_at = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now, sort_order=999
    )


class Board(Base, TimeStampMixin):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(75))
    notes: Mapped[List["Note"]] = relationship(back_populates="board")


class Note(Base, TimeStampMixin):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    board_id: Mapped[int] = mapped_column(
        ForeignKey("board.id", ondelete="CASCADE"), nullable=True
    )
    board: Mapped[List["Board"]] = relationship(back_populates="notes")
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0)
