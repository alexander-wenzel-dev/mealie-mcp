from enum import StrEnum


class AuthMethod(StrEnum):
    LDAP = "LDAP"
    MEALIE = "Mealie"
    OIDC = "OIDC"
    REVERSEPROXY = "ReverseProxy"

    def __str__(self) -> str:
        return str(self.value)
