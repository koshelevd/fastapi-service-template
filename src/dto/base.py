from datetime import datetime

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    ...


class ORMBaseSchema(BaseSchema):
    id: int = Field(default=1, example=1, description="Идентификатор")
    created_at: datetime = Field(example="2023-04-03T16:29:51.363289", description="Дата создания записи")
    updated_at: datetime | None = Field(example="2023-04-03T16:29:51.363289", description="Дата изменения записи")
    is_active: bool = Field(default=True, example=True, description="Признак логического удаления")

    class Config:
        orm_mode = True
