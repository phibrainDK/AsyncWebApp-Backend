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


class ModalType(str, Enum):
    GENERAL = "general"
    LIST = "list"


class OrderOption(str, Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


class ContentType(str, Enum):
    PDF = "application/pdf"
    PNG = "image/png"
    JPEG = "image/jpeg"
    GIF = "image/gif"


class FileType(str, Enum):
    ACCOUNT = "account"
    LOAN = "loan"