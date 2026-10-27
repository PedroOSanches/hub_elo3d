from pydantic import BaseModel
from uuid import UUID

class AuthResponseUser:

    id: UUID
    name: str
    email: str
    role: str
    access_token: str
    refresh_user: str
