from pydantic import BaseSettings

from enum import Enum


class StageOption(str, Enum):
    QA = "qa"
    PROD = "prod"
    DEV = "dev"
    LOCAL = "local"
    TEST = "test"

    def is_local_or_test_env(self):
        return self in [self.TEST, self.LOCAL]


class DatabaseOption(str, Enum):
    POSTGRES = "postgres"
    SQLITE = "sqlite"


class Settings(BaseSettings):
    DEPLOY_REGION: str = ""
    API_VERSION: str = "1.0"
    API_URL_PREFIX: str = "/api"
    ROOT_PATH: str = ""

    DEBUG: bool = True
    USE_SENTRY: bool = False
    SENTRY_DSN: str = ""
    ENV_STAGE: StageOption = StageOption.LOCAL

    class Config(BaseSettings.Config):
        env_file = ".env"


class AwsSettings(BaseSettings):
    APP_DYNAMODB_TABLE_VD: str = ""
    COGNITO_USER_POOL_ID: str = ""
    BACKEND_BUCKET_NAME: str = ""
    WEBSOCKETS_SERVER_NAME: str = ""
    class Config:
        env_file = ".env"


class DatabaseSettings(BaseSettings):
    # Database conection
    DATABASE: DatabaseOption = DatabaseOption.POSTGRES
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_NAME: str = "postgres"

    DEBUG: bool = True
    DEFAULT_PASSWORD: str = "password"

    ENV_STAGE: StageOption = StageOption.LOCAL

    class Config:
        env_file = ".env"


settings = Settings()
aws_settings = AwsSettings()
database_settings = DatabaseSettings()

settings.ROOT_PATH = (
    f"/{settings.ENV_STAGE}" if settings.ENV_STAGE != StageOption.LOCAL else ""
)
