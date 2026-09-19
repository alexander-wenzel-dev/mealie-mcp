from enum import StrEnum


class RelationalKeyword(StrEnum):
    CONTAINS_ALL = "CONTAINS ALL"
    IN = "IN"
    IS = "IS"
    IS_NOT = "IS NOT"
    LIKE = "LIKE"
    NOT_IN = "NOT IN"
    NOT_LIKE = "NOT LIKE"

    def __str__(self) -> str:
        return str(self.value)
