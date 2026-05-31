from enum import Enum


class RegisteredParser(str, Enum):
    BRUTE = "brute"
    NLP = "nlp"
    OPENAI = "openai"

    def __str__(self) -> str:
        return str(self.value)
