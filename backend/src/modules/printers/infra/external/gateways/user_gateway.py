from uuid import UUID

from src.modules.printers.domain.gateways.i_user_gateway import IUserGateway


class UserGateway(IUserGateway):
    #TEMPORARIO: aceita qualquer user_id

    #unica classe que reconhece user

    def exists(self, user_id: UUID) -> bool:
        return True