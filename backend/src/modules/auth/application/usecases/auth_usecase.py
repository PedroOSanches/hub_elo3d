from typing import Any

from src.modules.auth.domain.gateways.gateway_user_interface import IGatewayUser
from src.shared.utils.password_hasher import verificar_senha

class AuthUsecase:

    def __init__(self, gateway: IGatewayUser) -> None:
        self.gateway = gateway

    def __call__(self, *, email: str, password: str) ->  AuthResponseSchema:
            
            user = self.gateway.get_user_by_email(email=email)

            if verificar_senha(password, user.password_hash):
                pass