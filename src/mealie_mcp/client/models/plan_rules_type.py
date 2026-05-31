from enum import Enum


class PlanRulesType(str, Enum):
    BREAKFAST = "breakfast"
    DESSERT = "dessert"
    DINNER = "dinner"
    DRINK = "drink"
    LUNCH = "lunch"
    SIDE = "side"
    SNACK = "snack"
    UNSET = "unset"

    def __str__(self) -> str:
        return str(self.value)
