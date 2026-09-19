from enum import StrEnum


class ReportSummaryStatus(StrEnum):
    FAILURE = "failure"
    IN_PROGRESS = "in-progress"
    PARTIAL = "partial"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
