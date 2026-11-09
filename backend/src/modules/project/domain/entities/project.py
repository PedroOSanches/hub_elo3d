from uuid import uuid7, UUID
from datetime import date, datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, field_validator

from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.urgency_enum import Urgency
from src.modules.project.domain.enums.category_enum import Category
from src.modules.project.domain.entities.project_file import ProjectFile

def initial_order_status() -> dict[OrderStatus, datetime]:
    return {
        OrderStatus.WAITING_FOR_PARTNER: datetime.now(timezone.utc)
    }

class Project(BaseModel):
    id: UUID = Field(
        default_factory = uuid7,
        description = "ID do projeto"
    )

    title: str = Field(
        ...,
        min_length = 3,
        description = "Título do projeto"
    )

    date_end: date = Field(
        ...,
        description = "Prazo estimado para término do projeto"
    )

    pieces_quantity: int = Field(
        ...,
        gt = 0,
        description = "Quantidade de peças necessárias para o projeto"
    )

    category: Category = Field(
        ...,
        description = "Categoria do projeto"
    )

    description: str = Field(
        ...,
        min_length = 1,
        max_length = 280,
        description = "Descrição do projeto"
    )

    technical_info: str | None = Field(
        default = None,
        description = "Informações técnicas adicionais do projeto"
    )

    urgency: Urgency = Field(
        ...,
        description = "Nível de prioridade do projeto"
    )

    order_status: dict[OrderStatus, datetime] = Field(
        default_factory = initial_order_status,
        description = "Status do pedido e o timestamp de quando foi atualizado"
    )

    printer_id: UUID | None = Field(
        default = None,
        description = "ID da impressora associada ao projeto"
    )

    filament_id: UUID = Field(
        ...,
        description = "ID do filamento associado ao projeto"
    )

    files: list[ProjectFile] = Field(
        ...,
        min_length = 1,
        description = "Lista de arquivos anexados ao projeto"
    )

    @field_validator("description", mode = "before")
    @classmethod
    def strip_description(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    model_config = ConfigDict(
        extra = "forbid",
        populate_by_name = True
    )

    def register_order_status(self, status: OrderStatus) -> None:
        if not isinstance(status, OrderStatus):
            raise ValueError("Status inválido")

        if status in self.order_status:
            raise ValueError("Status já registrado")

        self.order_status[status] = datetime.now(timezone.utc)

    @property
    def current_order_status(self) -> OrderStatus:
        if not self.order_status:
            raise ValueError("Nenhum status registrado")

        return next(reversed(self.order_status))