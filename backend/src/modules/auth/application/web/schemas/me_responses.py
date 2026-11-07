from pydantic import BaseModel
from uuid import UUID

class MeResponseSchema(BaseModel):

    user_id: UUID
    role: str
    