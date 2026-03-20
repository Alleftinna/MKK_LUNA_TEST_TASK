from fastapi import HTTPException


class BaseException(HTTPException):
    """Базовый класс для прикладных исключений API."""

    status_code: int = 500
    detail: str = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)
