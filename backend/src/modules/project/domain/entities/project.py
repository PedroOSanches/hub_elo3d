from uuid import uuid4, UUID
from datetime import date

from pydantic import BaseModel, Field, ConfigDict, field_validator

from src.modules.project.domain.enums.order_status_enum import OrderStatus
from src.modules.project.domain.enums.production_status_enum import ProductionStatus
from src.modules.project.domain.enums.urgency_enum import Urgency


class Project(BaseModel):
    id: UUID = Field(
        default_factory = uuid4,
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

    category: str = Field(
        ...,
        min_length = 1,
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

    order_status: OrderStatus = Field(
        default = OrderStatus.WAITING_FOR_PARTNER,
        description = "Status do pedido do projeto"
    )

    production_status: ProductionStatus | None = Field(
        default = None,
        description = "Status da produção do projeto"
    )

    printer_id: UUID | None = Field(
        default = None,
        description = "ID da impressora associada ao projeto"
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