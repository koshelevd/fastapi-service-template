import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, func
from sqlalchemy.sql import expression

from db.declarative import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="Идентификатор")
    created_at = Column(
        DateTime,
        index=True,
        nullable=False,
        default=datetime.datetime.now,
        server_default=func.now(),
        comment="Дата и время создания",
    )
    updated_at = Column(
        DateTime,
        index=True,
        nullable=False,
        default=datetime.datetime.now,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Дата и время последнего обновления",
    )
    is_active = Column(
        Boolean,
        nullable=False,
        comment="Логическое удаление объекта",
        default=True,
        server_default=expression.true(),
    )

    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict_lower(self) -> dict:
        return {str.lower(c.name): getattr(self, c.name) for c in self.__table__.columns}

    def as_list(self, by_fields: set | None = None):
        fields = []
        if by_fields:
            by_fields.add("id")
        for key, value in self.as_dict().items():
            if by_fields and key not in by_fields:
                continue
            if isinstance(value, datetime.datetime):
                value = value.isoformat(timespec="seconds")
            fields.append({key: value})
        return fields
