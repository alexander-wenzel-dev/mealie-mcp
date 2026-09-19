from enum import StrEnum


class PlanRulesDay(StrEnum):
    FRIDAY = "friday"
    MONDAY = "monday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    THURSDAY = "thursday"
    TUESDAY = "tuesday"
    UNSET = "unset"
    WEDNESDAY = "wednesday"

    def __str__(self) -> str:
        return str(self.value)
