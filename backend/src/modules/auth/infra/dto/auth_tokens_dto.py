from dataclasses import dataclass


@dataclass
class RefreshTokenDTO:

    refresh_token: str
    active: bool