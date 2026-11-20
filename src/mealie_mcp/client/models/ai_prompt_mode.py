from enum import StrEnum


class AIPromptMode(StrEnum):
    APPEND = "append"
    OVERRIDE = "override"

    def __str__(self) -> str:
        return str(self.value)
