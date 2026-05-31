from enum import Enum


class WebhookType(str, Enum):
    MEALPLAN = "mealplan"

    def __str__(self) -> str:
        return str(self.value)
