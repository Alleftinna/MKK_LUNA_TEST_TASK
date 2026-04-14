from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.organization import Organization


class Activity(BaseModel):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="activities_level_1_3"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    parent: Mapped[Activity | None] = relationship(
        "Activity",
        remote_side="Activity.id",
        back_populates="children",
    )
    children: Mapped[list[Activity]] = relationship("Activity", back_populates="parent")
    organizations: Mapped[list[Organization]] = relationship(
        secondary="organization_activities",
        back_populates="activities",
    )
