from src.services.activity_service import ActivityService


def test_activity_service_contract() -> None:

    for method_name in ("get_by_id", "list", "list_tree", "get_descendant_ids"):
        assert hasattr(
            ActivityService, method_name
        ), f"ActivityService must implement method '{method_name}'"
