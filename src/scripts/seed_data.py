import argparse
import asyncio

from sqlalchemy import delete

from src.core.database import AsyncSessionLocal, engine_async
from src.core.logger import logger
from src.models.base import Base
from src.models.template_entity import TemplateEntity


async def ensure_tables() -> None:
    async with engine_async.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def clear_template_data() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(delete(TemplateEntity))
        await session.commit()


async def seed_template_data() -> None:
    async with AsyncSessionLocal() as session:
        first_entity = TemplateEntity(
            name="example-template-entity",
            description="Sample row for freshly cloned projects",
        )
        second_entity = TemplateEntity(
            name="second-template-entity",
            description="Another sample row that can be changed or removed",
        )
        session.add_all(
            [
                first_entity,
                second_entity,
            ]
        )
        await session.commit()


async def run(reset: bool) -> None:
    await ensure_tables()
    if reset:
        await clear_template_data()
        logger.info("Template entities have been cleared")
    await seed_template_data()
    logger.info("Template entities have been inserted successfully")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed database with template data",
    )
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Do not clear existing template data before seeding",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    asyncio.run(run(reset=not arguments.no_reset))
