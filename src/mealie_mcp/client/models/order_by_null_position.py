from enum import Enum


class OrderByNullPosition(str, Enum):
    FIRST = "first"
    LAST = "last"

    def __str__(self) -> str:
        return str(self.value)
