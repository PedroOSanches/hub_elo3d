from enum import Enum

class Category(str, Enum):
    ORTHOSIS = "orthosis"
    PROSTHESIS = "prosthesis"
    ACCESSORY = "accessory"
    ADAPTER = "adapter"
    OTHER = "other"