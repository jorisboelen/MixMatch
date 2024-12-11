from os import makedirs, path
from pathlib import Path
from pydantic import AmqpDsn, DirectoryPath, Field, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from typing import Literal

APPLICATION_BASE_DIRECTORY = Path(__file__).resolve().parent.parent
APPLICATION_ASSETS_DIRECTORY = path.join(APPLICATION_BASE_DIRECTORY, "assets")


class Settings(BaseSettings):
    BASE_DIRECTORY: Path = path.join(Path.home(), '.mixmatch')
    CORS_ALLOWED_ORIGINS: list[str] = Field(default_factory=list)
    IMAGE_DIRECTORY: Path = path.join(BASE_DIRECTORY, 'image')
    MUSIC_DIRECTORY: DirectoryPath = path.join(Path.home(), 'Music')
    SESSION_EXPIRE_SECONDS: int = 3600 * 24 * 60  # 60 days

    # database settings
    POSTGRES_SCHEME: Literal['postgresql'] = 'postgresql'
    POSTGRES_HOST: str = 'mixmatch-db'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'mixmatch'
    POSTGRES_USER: str = 'mixmatch'
    POSTGRES_PASSWORD: str = 'mixmatch'

    @computed_field
    @property
    def sqlalchemy_database_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.POSTGRES_SCHEME,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )

    # celery settings
    RABBITMQ_SCHEME: Literal['amqp', 'amqps'] = 'amqp'
    RABBITMQ_HOST: str = 'mixmatch-rabbitmq'
    RABBITMQ_PORT: int = 5672
    RABBITMQ_DEFAULT_USER: str = 'guest'
    RABBITMQ_DEFAULT_PASS: str = 'guest'

    @computed_field
    @property
    def celery_broker_dsn(self) -> AmqpDsn:
        return MultiHostUrl.build(
            scheme=self.RABBITMQ_SCHEME,
            username=self.RABBITMQ_DEFAULT_USER,
            password=self.RABBITMQ_DEFAULT_PASS,
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT
        )


settings = Settings(_env_file=('development.env', 'settings.env'), _env_file_encoding='utf-8')
makedirs(settings.BASE_DIRECTORY, exist_ok=True)
makedirs(settings.IMAGE_DIRECTORY, exist_ok=True)
