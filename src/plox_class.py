import typing as t
from enum import Enum
from typing import TYPE_CHECKING

from callable import PloxCallable
from plox_function import LoxFunction
from plox_instance import LoxInstance

if TYPE_CHECKING:
    from interpreter import Interpreter


class LoxClass(PloxCallable):
    def __init__(
        self,
        name: str,
        superclass: t.Optional["LoxClass"],
        methods: dict[str, LoxFunction],
    ):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def call(self, interpreter: "Interpreter", arguments: list) -> LoxInstance:
        instance = LoxInstance(self)

        initializer = self.get_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def get_method(self, name: str) -> LoxFunction:
        if name in self.methods:
            return self.methods[name]

        if self.superclass is not None:
            return self.superclass.get_method(name)

    def arity(self) -> int:
        initializer = self.get_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def __str__(self) -> str:
        return self.name


class ClassType(Enum):
    NONE = 0
    CLASS = 1
    SUBCLASS = 2
