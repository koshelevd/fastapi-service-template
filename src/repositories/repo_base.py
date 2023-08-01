from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from db.tables.base import BaseModel


class BaseRepository(ABC):
    """
    Базовый класс репозитория.

    Репозиторий НИКОГДА не комитит.
    Управлением транзакциями занимается слой БЛ.
    Это позволяет слою БЛ использовать методы репозитория последовательно, управляя транзакциями лично.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def is_exists(self, **kwargs):
        ...

    async def validate_uniques(self, obj: BaseModel) -> list[str]:
        exc_context = []
        for column in obj.__table__.columns:
            if column.unique and not column.name == "id":
                if column.nullable and getattr(obj, column.name) is None:
                    continue
                to_search = {column.name: getattr(obj, column.name)}
                if await self.is_exists(**to_search):
                    exc_context.append(column.name)

        return exc_context

    async def validate_uniques_by_values(self, model: type[BaseModel], obj_data: dict[str, Any]) -> list[str]:
        exc_context = []
        unique_columns = [column.name for column in model.__table__.columns if column.unique]
        for column, value in obj_data.items():
            if column in unique_columns and await self.is_exists(**{column: value}):
                exc_context.append(column)

        return exc_context
