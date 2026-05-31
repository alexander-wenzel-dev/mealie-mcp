from enum import Enum


class TimelineEventImage(str, Enum):
    DOES_NOT_HAVE_IMAGE = "does not have image"
    HAS_IMAGE = "has image"

    def __str__(self) -> str:
        return str(self.value)
