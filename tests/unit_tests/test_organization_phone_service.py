from src.services.organization_phone_service import OrganizationPhoneService


def test_organization_phone_service_contract() -> None:

    for method_name in ("get_by_id", "list_phones", "list_by_organization"):
        assert hasattr(
            OrganizationPhoneService, method_name
        ), f"OrganizationPhoneService must implement method '{method_name}'"
