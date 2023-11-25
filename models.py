from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime, func, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(Integer(), unique=True)
    moods: Mapped[List["Mood"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    is_admin: Mapped[bool] = mapped_column(Boolean())
    config: Mapped["Config"] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, tg_user_id={self.tg_user_id!r})"


class Mood(Base):
    __tablename__ = "mood"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    mood: Mapped[int] = mapped_column(Integer())
    user: Mapped["User"] = relationship(back_populates="moods")
    datetime_added: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    plus_factors: Mapped[Optional[str]] = mapped_column(String())
    minus_factors: Mapped[Optional[str]] = mapped_column(String())

    def __repr__(self) -> str:
        return f"Mood(id={self.id!r}, user_id={self.user_id!r}, mood={self.mood!r}, \
        datetime_added={self.datetime_added!r}, plus_factors={self.plus_factors!r}, \
        minus_factors={self.minus_factors!r})"


class Config(Base):
    __tablename__ = "config"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="config")
    notifications_on: Mapped[bool] = mapped_column(Boolean(), default=False)
    show_factors_on: Mapped[bool] = mapped_column(Boolean(), default=False)
    show_analytics_on: Mapped[bool] = mapped_column(Boolean(), default=True)

    def __repr__(self) -> str:
        return f"Config(id={self.id!r}, user_id={self.user_id!r}, notifications_on={self.notifications_on!r}, \
        show_factors_on={self.show_factors_on!r},show_analytics_on={self.show_analytics_on!r})"
