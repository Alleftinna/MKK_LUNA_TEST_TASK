from pydantic import BaseModel, ConfigDict


class OrganizationPhoneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    phone: str
    phone_description: str | None = None
