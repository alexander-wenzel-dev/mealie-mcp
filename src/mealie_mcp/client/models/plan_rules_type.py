from enum import StrEnum


class PlanRulesType(StrEnum):
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
