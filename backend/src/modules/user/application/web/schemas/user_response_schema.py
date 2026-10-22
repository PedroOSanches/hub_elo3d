from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.modules.user.domain.entities.endereco import Address
from src.modules.user.domain.enums.role_enum import ROLE

class UserResponseSchema(BaseModel):

    model_config = ConfigDict(
        use_enum_values=True,
        from_attributes=True
        )
    
    id: UUID
    name: str
    email: EmailStr
    phone: PhoneNumber
    address: Address
    institution_id: UUID | None
    role: ROLE