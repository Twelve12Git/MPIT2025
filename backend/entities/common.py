from enum import Enum
class ParameterType(Enum):
    NUM = "NUMBER"  # float(must have precision in config) or int
    BOOL = "BOOLEAN"