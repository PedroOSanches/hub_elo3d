from enum import Enum


class StatusImpressora(str, Enum):
    DISPONIVEL = "disponivel"
    EM_USO = "em uso"
    INATIVA = "inativa"