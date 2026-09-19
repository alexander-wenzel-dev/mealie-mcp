from enum import StrEnum


class LogicalOperator(StrEnum):
    AND = "AND"
    OR = "OR"

    def __str__(self) -> str:
        return str(self.value)
