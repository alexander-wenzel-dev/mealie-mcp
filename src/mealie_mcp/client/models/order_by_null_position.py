from enum import StrEnum


class OrderByNullPosition(StrEnum):
    FIRST = "first"
    LAST = "last"

    def __str__(self) -> str:
        return str(self.value)
