from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Building(BaseModel):
    __tablename__ = "buildings"

    address: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    organizations: Mapped[list["Organization"]] = relationship(back_populates="building")
