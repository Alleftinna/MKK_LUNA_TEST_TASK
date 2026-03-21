from src.services.building_service import BuildingService


def test_building_service_contract() -> None:

    for method_name in ("get_by_id", "list_buildings", "list_within_bbox", "list_within_radius"):
        assert hasattr(
            BuildingService, method_name
        ), f"BuildingService must implement method '{method_name}'"
