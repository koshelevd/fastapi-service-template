from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing_extensions import AsyncGenerator

from application.settings.broker import Settings as kafka_settings
from controllers.stub import Stub
from services.const import SERVICE_NAME
from services.event_constructor import EventConstructor
from services.uow import BaseUoW


async def get_session(sessionmaker: async_sessionmaker = Depends(Stub(async_sessionmaker))) -> AsyncGenerator:
    async with sessionmaker() as session:
        yield session


def get_kafka_producer_settings(
    kafka_app_settings: kafka_settings = Depends(Stub(kafka_settings)),
) -> ProducerSettings:
    return ProducerSettings(
        acks=kafka_app_settings.KAFKA_ACKS,
        bootstrap_servers=kafka_app_settings.KAFKA_SERVER,
        transactional_id=kafka_app_settings.TRANSACTIONAL_ID,
    )


def get_kafka_producer(
    producer_settings: ProducerSettings = Depends(get_kafka_producer_settings),
) -> KafkaProducer:
    return KafkaProducer(producer_settings)


def get_event_constructor(service_name: str = SERVICE_NAME) -> EventConstructor:
    return EventConstructor(service_name=service_name)


def get_uow(
    session: AsyncSession = Depends(get_session),
    producer: KafkaProducer = Depends(get_kafka_producer),
    kafka_app_settings: kafka_settings = Depends(Stub(kafka_settings)),
) -> BaseUoW:
    return BaseUoW(
        session=session,
        producer=producer,
        kafka_app_settings=kafka_app_settings,
    )
