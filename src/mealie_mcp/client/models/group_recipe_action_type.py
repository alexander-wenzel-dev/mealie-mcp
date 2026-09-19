from enum import StrEnum


class GroupRecipeActionType(StrEnum):
    LINK = "link"
    POST = "post"

    def __str__(self) -> str:
        return str(self.value)
