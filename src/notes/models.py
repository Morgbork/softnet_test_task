from sqlalchemy import DateTime, ForeignKey, Integer, String, event, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimeStampMixin(object):
    created_at = mapped_column(DateTime, default=func.now(), sort_order=999)
    updated_at = mapped_column(DateTime, default=func.now(), sort_order=999)

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = func.now()

    @classmethod
    async def __declare_last__(cls):
        event.listen(cls, "before_update", await cls._updated_at)


class Board(Base, TimeStampMixin):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(75))


class Note(Base, TimeStampMixin):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    board_id: Mapped[int] = mapped_column(
        ForeignKey("board.id", ondelete="CASCADE"), nullable=True
    )
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0)
