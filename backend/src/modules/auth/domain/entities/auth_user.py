from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class AuthUser:
    id: UUID
    email: str
    password_hash: str
    role: str