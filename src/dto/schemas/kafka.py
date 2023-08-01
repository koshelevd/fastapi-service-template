from enum import Enum

from pydantic import BaseModel


class EventType(str, Enum):
    POST = "POST"
    DELETE = "DELETE"
    PATCH = "PATCH"
    PUT = "PUT"


class EventData(BaseModel):
    before_change: list[dict]
    after_change: list[dict]


class HistoryEvent(BaseModel):
    event_date: str
    user_id: int
    event_type: EventType
    service_name: str
    target_entity: str
    event_data: EventData
