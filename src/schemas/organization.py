from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.schemas.activity import ActivityRead
from src.schemas.building import BuildingRead
from src.schemas.organization_phone import OrganizationPhoneRead


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    building: BuildingRead
    phones: list[OrganizationPhoneRead]
    activities: list[ActivityRead]


class OrganizationSearchByName(BaseModel):
    name: str = Field(min_length=1)


class OrganizationSearchByRadius(BaseModel):
    latitude: float
    longitude: float
    radius_m: float = Field(gt=0)


class OrganizationSearchByBbox(BaseModel):
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float

    @model_validator(mode="after")
    def validate_bounds(self) -> Self:
        if self.min_lat >= self.max_lat:
            raise ValueError("min_lat must be less than max_lat")
        if self.min_lon >= self.max_lon:
            raise ValueError("min_lon must be less than max_lon")
        return self


__all__ = (
    "OrganizationPhoneRead",
    "OrganizationRead",
    "OrganizationSearchByName",
    "OrganizationSearchByRadius",
    "OrganizationSearchByBbox",
)
