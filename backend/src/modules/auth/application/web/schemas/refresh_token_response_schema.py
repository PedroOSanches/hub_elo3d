from dataclasses import dataclass


@dataclass
class RefreshTokenResponseSchema:

    access_token: str
    