from enum import StrEnum


class ReportCategory(StrEnum):
    BACKUP = "backup"
    BULK_IMPORT = "bulk_import"
    MIGRATION = "migration"
    RESTORE = "restore"

    def __str__(self) -> str:
        return str(self.value)
