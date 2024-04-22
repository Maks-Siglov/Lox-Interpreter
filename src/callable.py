import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import stmt
from environment import Environment
from exceptions import Return

if TYPE_CHECKING:
    from interpreter import Interpreter


class PloxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> Any:
        pass


class LoxFunction(PloxCallable):
    def __init__(self, declaration: stmt.Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter: "Interpreter", arguments: list[Any]):
        environment = Environment(self.closure)
        for i in range(self.arity()):
            parameter_name = self.declaration.params[i].lexeme
            argument_value = arguments[i] if i < len(arguments) else None
            environment.define_var(parameter_name, argument_value)
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value

        return None

    def __str__(self) -> str:
        return f"<{self.declaration.name.lexeme}>"


class ClockCallable(PloxCallable):
    def arity(self):
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> float:
        return time.time()

    def __str__(self):
        return "<native fn>"
