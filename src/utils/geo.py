from dataclasses import dataclass
from math import cos, radians
from typing import Any

from sqlalchemy import func

EARTH_RADIUS_M = 6_371_000


@dataclass(frozen=True)
class BoundingBox:
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float


def build_bounding_box(
    latitude: float, longitude: float, radius_m: float
) -> BoundingBox:
    lat_delta = radius_m / 111_320
    cos_lat = max(0.0001, abs(cos(radians(latitude))))
    lon_delta = radius_m / (111_320 * cos_lat)
    return BoundingBox(
        min_lat=max(-90.0, latitude - lat_delta),
        max_lat=min(90.0, latitude + lat_delta),
        min_lon=max(-180.0, longitude - lon_delta),
        max_lon=min(180.0, longitude + lon_delta),
    )


def great_circle_distance_expression(
    latitude: float,
    longitude: float,
    latitude_column: Any,
    longitude_column: Any,
) -> Any:
    cosine_distance = func.sin(func.radians(latitude)) * func.sin(
        func.radians(latitude_column)
    ) + func.cos(func.radians(latitude)) * func.cos(
        func.radians(latitude_column)
    ) * func.cos(
        func.radians(longitude_column) - func.radians(longitude)
    )
    clamped_cosine_distance = func.least(
        1.0,
        func.greatest(-1.0, cosine_distance),
    )
    return EARTH_RADIUS_M * func.acos(clamped_cosine_distance)
