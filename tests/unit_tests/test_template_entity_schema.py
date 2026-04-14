from datetime import datetime, timezone

from src.schemas.template_entity import TemplateEntityCreate, TemplateEntityRead


def test_template_entity_create_schema_accepts_valid_payload() -> None:
    payload = TemplateEntityCreate(name="starter-entity", description="base template")
    assert payload.name == "starter-entity"
    assert payload.description == "base template"


def test_template_entity_read_schema_supports_from_attributes() -> None:
    timestamp = datetime.now(timezone.utc)
    payload = TemplateEntityRead.model_validate(
        {
            "id": 7,
            "name": "starter-entity",
            "description": "base template",
            "created_at": timestamp,
            "updated_at": timestamp,
        }
    )
    assert payload.id == 7
    assert payload.name == "starter-entity"
