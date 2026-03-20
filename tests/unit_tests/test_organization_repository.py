from src.repositories.organization_repository import OrganizationRepository


def test_organization_repository_contract() -> None:

    for method_name in (
        "get_by_id",
        "list",
        "list_by_building",
        "list_by_activity",
        "search_by_name",
        "search_by_radius",
        "search_by_bbox",
    ):
        assert hasattr(
            OrganizationRepository, method_name
        ), f"OrganizationRepository must implement method '{method_name}'"
