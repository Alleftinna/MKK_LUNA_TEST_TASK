import pytest
from pydantic import ValidationError

from src.schemas.activity import ActivityRead


def test_activity_read_schema_validates_level() -> None:

    valid_payload = ActivityRead.model_validate(
        {"id": 10, "name": "Food", "level": 1, "parent_id": None}
    )
    assert valid_payload.level == 1

    with pytest.raises(ValidationError):
        ActivityRead.model_validate(
            {"id": 11, "name": "Invalid", "level": 4, "parent_id": 1}
        )
