import typing as t
from enum import Enum

import stmt
from callable import PloxCallable
from environment import Environment
from exceptions import ReturnError
from plox_instance import LoxInstance

if t.TYPE_CHECKING:
    from interpreter import Interpreter


class LoxFunction(PloxCallable):
    def __init__(
        self,
        declaration: stmt.Function,
        closure: Environment,
        is_initializer: bool,
    ):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(
        self,
        interpreter: "Interpreter",
        arguments: list[t.Any],
    ) -> t.Any:
        environment = Environment(self.closure)
        for i in range(self.arity()):
            parameter_name = self.declaration.params[i].lexeme
            argument_value = arguments[i] if i < len(arguments) else None
            environment.define_var(parameter_name, argument_value)
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnError as return_value:
            return return_value.value

        if self.is_initializer:
            return self.closure.get_at(0, "self")

    def bind(self, instance: LoxInstance) -> "LoxFunction":
        environment = Environment(self.closure)
        environment.define_var("self", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def __str__(self) -> str:
        return f"<{self.declaration.name.lexeme}>"


class FunctionType(Enum):
    NONE = 0
    FUNCTION = 1
    METHOD = 2
    INITIALIZER = 3
