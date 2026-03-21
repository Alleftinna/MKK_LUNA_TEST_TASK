from src.repositories.organization_phone_repository import OrganizationPhoneRepository


def test_organization_phone_repository_contract() -> None:

    for method_name in ("get_by_id", "list", "list_by_organization"):
        assert hasattr(
            OrganizationPhoneRepository, method_name
        ), f"OrganizationPhoneRepository must implement method '{method_name}'"
