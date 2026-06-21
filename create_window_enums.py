from enum import Enum

class TypeComboValues(Enum):
    COPY = "copy"
    DELETE = "delete"
    MOVE = "move"

class IntervalTypeComboValues(Enum):
    S = "seconds"
    MIN = "minutes"
    H = "hours"
    D = "days"
    MON = "months"