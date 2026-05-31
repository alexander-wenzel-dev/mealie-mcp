from enum import Enum


class GroupRecipeActionType(str, Enum):
    LINK = "link"
    POST = "post"

    def __str__(self) -> str:
        return str(self.value)
