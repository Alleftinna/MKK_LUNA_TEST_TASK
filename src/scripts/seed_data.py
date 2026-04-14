from __future__ import annotations

import argparse
import asyncio

from sqlalchemy import delete

from src.core.database import AsyncSessionLocal, engine_async
from src.core.logger import logger
from src.models.activity import Activity
from src.models.base import Base
from src.models.building import Building
from src.models.organization import Organization, OrganizationActivity
from src.models.organization_phone import OrganizationPhone


async def ensure_tables() -> None:
    async with engine_async.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def clear_directory_data() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(delete(OrganizationPhone))
        await session.execute(delete(OrganizationActivity))
        await session.execute(delete(Organization))
        await session.execute(delete(Activity))
        await session.execute(delete(Building))
        await session.commit()


async def seed_directory_data() -> None:
    async with AsyncSessionLocal() as session:
        # Здания
        building_1 = Building(
            address="г. Москва, ул. Ленина 1, офис 3",
            latitude=55.7558,
            longitude=37.6176,
        )
        building_2 = Building(
            address="г. Москва, ул. Блюхера, 32/1",
            latitude=55.8101,
            longitude=37.5023,
        )
        building_3 = Building(
            address="г. Санкт-Петербург, Невский проспект, 10",
            latitude=59.9343,
            longitude=30.3351,
        )

        # Деятельности (не глубже 3 уровней)
        food = Activity(name="Еда", level=1, parent_id=None)
        meat = Activity(name="Мясная продукция", level=2, parent=food)
        milk = Activity(name="Молочная продукция", level=2, parent=food)

        cars = Activity(name="Автомобили", level=1, parent_id=None)
        trucks = Activity(name="Грузовые", level=2, parent=cars)
        passenger = Activity(name="Легковые", level=2, parent=cars)
        spare_parts = Activity(name="Запчасти", level=3, parent=passenger)
        accessories = Activity(name="Аксессуары", level=3, parent=passenger)

        # Организации
        org_1 = Organization(
            name='ООО "Рога и Копыта"',
            building=building_1,
            activities=[food, meat],
            phones=[
                OrganizationPhone(phone="2-222-222", phone_description="Приемная"),
                OrganizationPhone(phone="3-333-333", phone_description="Отдел продаж"),
            ],
        )
        org_2 = Organization(
            name='ООО "Молочный Мир"',
            building=building_2,
            activities=[food, milk],
            phones=[
                OrganizationPhone(
                    phone="8-923-666-13-13", phone_description="Горячая линия"
                )
            ],
        )
        org_3 = Organization(
            name='ООО "АвтоБаза"',
            building=building_1,
            activities=[cars, trucks],
            phones=[
                OrganizationPhone(
                    phone="8-800-100-20-30", phone_description="Диспетчер"
                )
            ],
        )
        org_4 = Organization(
            name='ООО "Легковой Сервис"',
            building=building_3,
            activities=[cars, passenger, spare_parts, accessories],
            phones=[
                OrganizationPhone(phone="8-812-555-00-11", phone_description="Сервис"),
                OrganizationPhone(phone="8-812-555-00-12", phone_description="Склад"),
            ],
        )

        session.add_all(
            [
                building_1,
                building_2,
                building_3,
                food,
                meat,
                milk,
                cars,
                trucks,
                passenger,
                spare_parts,
                accessories,
                org_1,
                org_2,
                org_3,
                org_4,
            ]
        )
        await session.commit()


async def run(reset: bool) -> None:
    await ensure_tables()
    if reset:
        await clear_directory_data()
        logger.info("Directory data has been cleared")
    await seed_directory_data()
    logger.info("Test data has been inserted successfully")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed database with directory test data",
    )
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Do not clear existing directory data before seeding",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    asyncio.run(run(reset=not arguments.no_reset))
