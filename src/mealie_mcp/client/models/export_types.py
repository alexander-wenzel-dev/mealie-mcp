from enum import StrEnum


class ExportTypes(StrEnum):
    JSON = "json"

    def __str__(self) -> str:
        return str(self.value)
