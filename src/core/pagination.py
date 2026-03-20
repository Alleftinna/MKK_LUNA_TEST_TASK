from collections.abc import Sequence

from pydantic import BaseModel, Field


class PageMeta(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total: int = Field(ge=0)
    pages: int = Field(ge=0)


class Page[T](BaseModel):
    items: Sequence[T]
    meta: PageMeta


def paginate_params(page: int | None, page_size: int | None) -> tuple[int, int]:
    current_page = max(1, page or 1)
    current_size = max(1, min(100, page_size or 20))
    return current_page, current_size
