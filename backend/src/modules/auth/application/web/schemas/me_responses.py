from uuid import UUID

from pydantic import BaseModel


class MeResponseSchema(BaseModel):

    user_id: UUID
    role: str
    