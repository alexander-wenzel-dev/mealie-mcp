from enum import StrEnum


class TimelineEventType(StrEnum):
    COMMENT = "comment"
    INFO = "info"
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
