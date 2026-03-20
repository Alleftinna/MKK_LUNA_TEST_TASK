from pydantic import BaseModel, ConfigDict, Field


class ActivityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    level: int = Field(ge=1, le=3)
    parent_id: int | None = None
