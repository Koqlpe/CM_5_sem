#  enum_create.py
from enum import Enum, auto

class Method(Enum):
    bisection = auto()
    simple_iteration = auto()
    newton = auto()