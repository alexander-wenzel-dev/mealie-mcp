from enum import StrEnum


class ImageType(StrEnum):
    MIN_ORIGINAL_WEBP = "min-original.webp"
    ORIGINAL_WEBP = "original.webp"
    TINY_ORIGINAL_WEBP = "tiny-original.webp"

    def __str__(self) -> str:
        return str(self.value)
