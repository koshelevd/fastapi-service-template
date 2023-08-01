from kafka_adapter import KafkaProducer
from sqlalchemy.ext.asyncio import AsyncSession

from application.settings.broker import Settings as kafka_settings
from repositories.uow_base import KafkaProducerBaseUoW, SQLAlchemyBaseUoW


class BaseUoW(
    SQLAlchemyBaseUoW,
    KafkaProducerBaseUoW,
):
    def __init__(
        self,
        session: AsyncSession,
        producer: KafkaProducer,
        kafka_app_settings: kafka_settings,
    ) -> None:
        SQLAlchemyBaseUoW.__init__(self, session)
        KafkaProducerBaseUoW.__init__(self, producer, kafka_app_settings)
