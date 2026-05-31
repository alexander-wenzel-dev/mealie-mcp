from enum import Enum


class ReportSummaryStatus(str, Enum):
    FAILURE = "failure"
    IN_PROGRESS = "in-progress"
    PARTIAL = "partial"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
