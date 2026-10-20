from enum import Enum


class StatusPrinter(str, Enum):
    DISPONIVEL = "disponivel"
    EM_USO = "em uso"
    INATIVA = "inativa"