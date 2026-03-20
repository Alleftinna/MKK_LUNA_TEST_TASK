from src.schemas.building import BuildingRead

def test_building_read_schema() -> None:
    payload = BuildingRead.model_validate(
        {
            "id": 1,
            "address": "Moscow, Lenina 1",
            "latitude": 55.7558,
            "longitude": 37.6176,
        }
    )
    assert payload.id == 1
    assert payload.address == "Moscow, Lenina 1"
