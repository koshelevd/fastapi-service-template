from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_NAME: str = "postgres"
    DB_PORT: int = 5432

    def get_db_url(self, async_mode: bool = True):
        return PostgresDsn.build(
            scheme="postgresql+asyncpg" if async_mode else "postgresql",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            path=f"/{self.DB_NAME}",
            port=str(self.DB_PORT),
        )
