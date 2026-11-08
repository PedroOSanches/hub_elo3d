from typing import Any

from src.modules.user.domain.entities.user import User

class UserDTO:

    @classmethod
    def entitie_to_dict(cls, user: User) -> tuple[dict[str, Any], dict[str, Any]]:

        user_data: dict[str, Any] = user.model_dump(mode='json')
        address_data = user.address.model_dump(mode='json')
        user_data.pop('address')

        return user_data, address_data

    @classmethod
    def dict_to_entitie(cls, user_db: dict[str, Any]) -> User:

        user: dict[str, Any] = user_db.get('user', {})
        address = user_db.get('address', {})

        user['address'] = address

        return User.model_validate(user)