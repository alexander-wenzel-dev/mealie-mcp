from enum import Enum


class ImageType(str, Enum):
    MIN_ORIGINAL_WEBP = "min-original.webp"
    ORIGINAL_WEBP = "original.webp"
    TINY_ORIGINAL_WEBP = "tiny-original.webp"

    def __str__(self) -> str:
        return str(self.value)
