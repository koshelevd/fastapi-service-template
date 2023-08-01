from abc import ABC, abstractmethod

from kafka_adapter import ProducerEvent

from dto.schemas.kafka import HistoryEvent


class UoWDataBaseInterface(ABC):
    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...


class UoWKafkaProducerBaseInterface(ABC):
    @abstractmethod
    async def send(self, event: ProducerEvent) -> None:
        ...

    @property
    @abstractmethod
    def topic(self) -> str:
        ...


class EventConstructorInterface(ABC):
    @abstractmethod
    def create_producer_event(self, *args, **kwargs) -> ProducerEvent:
        ...

    @abstractmethod
    def create_history_event(self, *args, **kwargs) -> HistoryEvent:
        ...
