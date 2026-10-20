from uuid import uuid4, UUID
from datetime import date

from pydantic import BaseModel, Field, ConfigDict

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

    model_config = ConfigDict(
        extra = "forbid",
        populate_by_name = True
    )