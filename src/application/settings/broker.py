from pydantic import BaseSettings


class Settings(BaseSettings):
    KAFKA_SERVER: str = "localhost:9092"
    KAFKA_TOPIC: str = "Test"
    TRANSACTIONAL_ID = "EXAMPLE-SERVICE"
    KAFKA_ACKS: str = "all"
