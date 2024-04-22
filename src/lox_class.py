from typing import TYPE_CHECKING

from callable import PloxCallable
from lox_instance import LoxInstance

if TYPE_CHECKING:
    from interpreter import Interpreter


class LoxClass(PloxCallable):
    def __init__(self, name: str):
        self.name = name

    def call(self, interpreter: "Interpreter", arguments: list):
        instance = LoxInstance(self)
        return instance

    def arity(self):
        return 0

    def __str__(self) -> str:
        return self.name

