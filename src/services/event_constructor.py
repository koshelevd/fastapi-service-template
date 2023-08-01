from datetime import datetime, timezone
from typing import Any

from kafka_adapter import ProducerEvent

from dto.schemas.kafka import EventData, EventType, HistoryEvent
from services.interfaces import EventConstructorInterface


class EventConstructor(EventConstructorInterface):
    def __init__(self, service_name: str):
        self.service_name = service_name

    def create_producer_event(self, topic: str, value: str | dict[str, Any]) -> ProducerEvent:
        return ProducerEvent(topic=topic, value=value)

    def create_history_event(
        self,
        target_entity: str,
        event_type: EventType,
        after: list[dict],
        before: list[dict] = None,
        user_id: int = None,
    ) -> HistoryEvent:
        return HistoryEvent(
            event_date=datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(timespec="seconds"),
            # TODO: убрать заглушку user_id
            user_id=user_id or 1,
            event_type=event_type,
            service_name=self.service_name,
            target_entity=target_entity,
            event_data=EventData(before_change=before if before else [], after_change=after),
        )
