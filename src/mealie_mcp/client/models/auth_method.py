from enum import Enum


class AuthMethod(str, Enum):
    LDAP = "LDAP"
    MEALIE = "Mealie"
    OIDC = "OIDC"

    def __str__(self) -> str:
        return str(self.value)
