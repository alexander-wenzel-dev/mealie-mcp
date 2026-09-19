from enum import StrEnum


class PlanEntryType(StrEnum):
    BREAKFAST = "breakfast"
    DESSERT = "dessert"
    DINNER = "dinner"
    DRINK = "drink"
    LUNCH = "lunch"
    SIDE = "side"
    SNACK = "snack"

    def __str__(self) -> str:
        return str(self.value)
