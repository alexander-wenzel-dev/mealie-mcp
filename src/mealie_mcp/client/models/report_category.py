from enum import Enum


class ReportCategory(str, Enum):
    BACKUP = "backup"
    BULK_IMPORT = "bulk_import"
    MIGRATION = "migration"
    RESTORE = "restore"

    def __str__(self) -> str:
        return str(self.value)
