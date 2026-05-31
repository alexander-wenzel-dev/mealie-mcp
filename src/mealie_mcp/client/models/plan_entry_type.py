from enum import Enum


class PlanEntryType(str, Enum):
    BREAKFAST = "breakfast"
    DESSERT = "dessert"
    DINNER = "dinner"
    DRINK = "drink"
    LUNCH = "lunch"
    SIDE = "side"
    SNACK = "snack"

    def __str__(self) -> str:
        return str(self.value)
