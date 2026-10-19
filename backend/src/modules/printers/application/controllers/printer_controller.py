from uuid import UUID

from src.modules.impressoras.application.viewmodels.impressora_viewmodel import (
    ImpressoraViewModel,
)
from src.modules.impressoras.application.web.schemas.impressora_schemas import (
    AtualizarImpressoraRequest,
    CriarImpressoraRequest,
    ImpressoraResponse,
)
from src.modules.impressoras.domain.entities.impressora import Impressora
from src.modules.impressoras.domain.errors.impressora_errors import (
    ImpressoraNotFoundError,
    UsuarioNotFoundError,
)
from src.modules.impressoras.domain.gateways.i_usuario_gateway import IUsuarioGateway
from src.modules.impressoras.domain.repositories.i_impressora_repository import (
    IImpressoraRepository,
)


class ImpressoraController:
    
    def __init__(
        self,
        repository: IImpressoraRepository,
        usuario_gateway: IUsuarioGateway,
    ) -> None:
        self._repository = repository
        self._usuario_gateway = usuario_gateway

    def criar(self, request: CriarImpressoraRequest) -> ImpressoraResponse:
        if not self._usuario_gateway.exists(request.usuario_id):
            raise UsuarioNotFoundError(request.usuario_id)
        impressora = Impressora(**request.model_dump())
        self._repository.criar(impressora)
        return ImpressoraViewModel.from_entity(impressora)

    def obter(self, impressora_id: UUID) -> ImpressoraResponse:
        return ImpressoraViewModel.from_entity(self._buscar_ou_falhar(impressora_id))

    def listar(self, usuario_id: UUID | None = None) -> list[ImpressoraResponse]:
        return ImpressoraViewModel.from_entities(self._repository.listar(usuario_id))

    def atualizar(
        self, impressora_id: UUID, request: AtualizarImpressoraRequest) -> ImpressoraResponse:
        atual = self._buscar_ou_falhar(impressora_id)
        dados = {**atual.model_dump(), **request.model_dump(exclude_none=True)}
        atualizada = Impressora(**dados)
        self._repository.atualizar(atualizada)
        return ImpressoraViewModel.from_entity(atualizada)

    def deletar(self, impressora_id: UUID) -> None:
        self._buscar_ou_falhar(impressora_id)
        self._repository.deletar(impressora_id)

    def _buscar_ou_falhar(self, impressora_id: UUID) -> Impressora:
        impressora = self._repository.buscar_por_id(impressora_id)
        if impressora is None:
            raise ImpressoraNotFoundError(impressora_id)
        return impressora