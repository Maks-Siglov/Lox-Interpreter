from enum import Enum
from typing import TYPE_CHECKING

from callable import PloxCallable
from plox_function import LoxFunction
from plox_instance import LoxInstance

if TYPE_CHECKING:
    from interpreter import Interpreter


class LoxClass(PloxCallable):
    def __init__(self, name: str, methods: [str, LoxFunction]):
        self.name = name
        self.methods = methods

    def call(self, interpreter: "Interpreter", arguments: list):
        instance = LoxInstance(self)

        initializer = self.get_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def get_method(self, name: str):
        if name in self.methods:
            return self.methods[name]

    def arity(self):
        initializer = self.get_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def __str__(self) -> str:
        return self.name


class ClassType(Enum):
    NONE = 0
    CLASS = 1
