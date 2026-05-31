from enum import Enum


class TimelineEventType(str, Enum):
    COMMENT = "comment"
    INFO = "info"
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
