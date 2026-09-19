from enum import StrEnum


class RegisteredParser(StrEnum):
    BRUTE = "brute"
    NLP = "nlp"
    OPENAI = "openai"

    def __str__(self) -> str:
        return str(self.value)
