import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime]
    status: Mapped[str] = mapped_column(default="alive")
    status_updated_at: Mapped[datetime.datetime]
