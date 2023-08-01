from kafka_adapter import KafkaProducer, ProducerEvent
from sqlalchemy.ext.asyncio import AsyncSession

from application.settings.broker import Settings as kafka_settings
from services.interfaces import UoWDataBaseInterface, UoWKafkaProducerBaseInterface


class SQLAlchemyBaseUoW(UoWDataBaseInterface):
    """
    Базовый класс UoW (Unit of Work).

    Определяющий логическую транзакцию, т.е. атомарную синхронизацию изменений в объектах.
    Это позволяет слою БЛ управлять транзакциями лично.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


class KafkaProducerBaseUoW(UoWKafkaProducerBaseInterface):
    """
    Базовый класс UoW Kafka, отправляющий ивенты (сообщения) через продюсера в заданный топик.
    """

    def __init__(self, producer: KafkaProducer, kafka_app_settings: kafka_settings) -> None:
        self.producer = producer
        self.kafka_app_settings = kafka_app_settings

    async def send(self, event: ProducerEvent) -> None:
        if settings.IS_KAFKA_ON:
            await self.producer.start(event)
        else:
            logger.info(f"Sent to kafka {event}")

    @property
    def topic(self) -> str:
        return self.kafka_app_settings.KAFKA_TOPIC
