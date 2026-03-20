from src.repositories.activity_repository import ActivityRepository


def test_activity_repository_contract() -> None:

    for method_name in ("get_by_id", "list", "get_descendant_ids", "list_tree"):
        assert hasattr(
            ActivityRepository, method_name
        ), f"ActivityRepository must implement method '{method_name}'"
