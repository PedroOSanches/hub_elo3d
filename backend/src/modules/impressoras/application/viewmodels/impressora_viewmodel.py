from src.modules.impressoras.application.web.schemas.impressora_schemas import (
    ImpressoraResponse,)
from src.modules.impressoras.domain.entities.impressora import Impressora


class ImpressoraViewModel:

    @staticmethod
    def from_entity(entity: Impressora) -> ImpressoraResponse:
        return ImpressoraResponse(
            id=entity.id,
            apelido=entity.apelido,
            modelo=entity.modelo,
            tecnologia_impressao=entity.tecnologia_impressao,
            usuario_id=entity.usuario_id,
            filamentos_aceitos=list(entity.filamentos_aceitos),
            status=entity.status,
        )

    @staticmethod
    def from_entities(entities: list[Impressora]) -> list[ImpressoraResponse]:
        return [ImpressoraViewModel.from_entity(e) for e in entities]