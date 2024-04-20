import time
from abc import ABC, abstractmethod

import stmt
from environment import Environment


class PloxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments: list):
        pass


class LoxFunction(PloxCallable):
    def __init__(self, declaration: stmt.Function):
        self.declaration = declaration

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments: list):
        environment = Environment(interpreter.globals)
        for i in range(self.arity()):
            parameter_name = self.declaration.params[i].lexeme
            argument_value = arguments[i] if i < len(arguments) else None
            environment.define_var(parameter_name, argument_value)
        interpreter.execute_block(self.declaration.body, environment)
        return None

    def __str__(self) -> str:
        return f"<{self.declaration.name.lexeme}>"


class ClockCallable(PloxCallable):
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<native fn>"
