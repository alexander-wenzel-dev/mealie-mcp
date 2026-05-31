from enum import Enum


class SupportedMigrations(str, Enum):
    CHOWDOWN = "chowdown"
    COOKN = "cookn"
    COPYMETHAT = "copymethat"
    MEALIE_ALPHA = "mealie_alpha"
    MYRECIPEBOX = "myrecipebox"
    NEXTCLOUD = "nextcloud"
    PAPRIKA = "paprika"
    PLANTOEAT = "plantoeat"
    RECIPEKEEPER = "recipekeeper"
    TANDOOR = "tandoor"

    def __str__(self) -> str:
        return str(self.value)
