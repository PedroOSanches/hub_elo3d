from enum import StrEnum


class Category(StrEnum):
    ORTHOSIS = "orthosis"
    PROSTHESIS = "prosthesis"
    ACCESSORY = "accessory"
    ADAPTER = "adapter"
    OTHER = "other"