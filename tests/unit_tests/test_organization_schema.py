import pytest
from pydantic import ValidationError

from src.schemas.organization import OrganizationPhoneRead, OrganizationRead, OrganizationSearchByName, OrganizationSearchByRadius, OrganizationSearchByBbox
from src.schemas.building import BuildingRead
from src.schemas.activity import ActivityRead


def test_organization_phone_read_schema() -> None:
    payload = OrganizationPhoneRead.model_validate(
        {
            "id": 1,
            "organization_id": 3,
            "phone": "8-923-666-13-13",
            "phone_description": "Sales",
        }
    )
    assert payload.phone == "8-923-666-13-13"
    assert payload.phone_description == "Sales"


def test_organization_read_schema_with_relations() -> None:
    payload = OrganizationRead.model_validate(
        {
            "id": 5,
            "name": 'OOO "Roga i Kopyta"',
            "building": BuildingRead.model_validate(
                {
                    "id": 7,
                    "address": "Moscow, Lenina 1, office 3",
                    "latitude": 55.7558,
                    "longitude": 37.6176,
                }
            ),
            "phones": [
                OrganizationPhoneRead.model_validate(
                    {
                        "id": 10,
                        "organization_id": 5,
                        "phone": "2-222-222",
                        "phone_description": "Reception",
                    }
                ),
                OrganizationPhoneRead.model_validate(
                    {
                        "id": 11,
                        "organization_id": 5,
                        "phone": "3-333-333",
                        "phone_description": "Support",
                    }
                ),
            ],
            "activities": [
                ActivityRead.model_validate(
                    {"id": 1, "name": "Food", "level": 1, "parent_id": None}
                ),
                ActivityRead.model_validate(
                    {"id": 2, "name": "Milk products", "level": 2, "parent_id": 1}
                ),
            ],
        }
    )

    assert payload.name == 'OOO "Roga i Kopyta"'
    assert len(payload.phones) == 2
    assert len(payload.activities) == 2


def test_organization_search_by_name_schema() -> None:
    valid_payload = OrganizationSearchByName.model_validate({"name": "Roga"})
    assert valid_payload.name == "Roga"

    with pytest.raises(ValidationError):
        OrganizationSearchByName.model_validate({"name": ""})


def test_organization_search_by_radius_schema() -> None:
    payload = OrganizationSearchByRadius.model_validate(
        {"latitude": 55.7, "longitude": 37.6, "radius_m": 500}
    )
    assert payload.radius_m == 500

    with pytest.raises(ValidationError):
        OrganizationSearchByRadius.model_validate(
            {"latitude": 55.7, "longitude": 37.6, "radius_m": 0}
        )


def test_organization_search_by_bbox_schema() -> None:
    payload = OrganizationSearchByBbox.model_validate(
        {"min_lat": 55.5, "max_lat": 56.0, "min_lon": 37.0, "max_lon": 38.0}
    )
    assert payload.min_lat < payload.max_lat
    assert payload.min_lon < payload.max_lon
