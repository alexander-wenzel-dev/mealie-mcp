from enum import StrEnum


class WebhookType(StrEnum):
    MEALPLAN = "mealplan"

    def __str__(self) -> str:
        return str(self.value)
