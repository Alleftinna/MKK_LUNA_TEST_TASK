from src.repositories.building_repository import BuildingRepository


def test_building_repository_contract() -> None:

    for method_name in (
        "get_by_id",
        "list_all",
        "list_within_bbox",
        "list_within_radius",
    ):
        assert hasattr(
            BuildingRepository, method_name
        ), f"BuildingRepository must implement method '{method_name}'"
