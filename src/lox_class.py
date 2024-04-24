from enum import Enum
from typing import TYPE_CHECKING

from callable import PloxCallable, LoxFunction
from lox_instance import LoxInstance

if TYPE_CHECKING:
    from interpreter import Interpreter


class LoxClass(PloxCallable):
    def __init__(self, name: str, methods: [str, LoxFunction]):
        self.name = name
        self.methods = methods

    def call(self, interpreter: "Interpreter", arguments: list):
        instance = LoxInstance(self)
        return instance

    def get_method(self, name: str):
        if name in self.methods:
            return self.methods[name]

    def arity(self):
        return 0

    def __str__(self) -> str:
        return self.name


class ClassType(Enum):
    NONE = 0
    CLASS = 1
