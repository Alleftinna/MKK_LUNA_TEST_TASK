from src.services.organization_service import OrganizationService


def test_organization_service_contract() -> None:

    for method_name in (
        "get_by_id",
        "list_by_building",
        "list_by_activity",
        "search_by_name",
        "search_by_radius",
        "search_by_bbox",
    ):
        assert hasattr(
            OrganizationService, method_name
        ), f"OrganizationService must implement method '{method_name}'"
