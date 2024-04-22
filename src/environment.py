from typing import Any

from plox_token import Token


class Environment:
    def __init__(self, enclosing=None):
        self.var_values = {}
        self.enclosing = enclosing

    def define_var(self, name, value) -> None:
        self.var_values[name] = value

    def get_var(self, name: Token) -> Any:
        if name.lexeme in self.var_values:
            return self.var_values[name.lexeme]
        elif self.enclosing is not None:
            return self.enclosing.get_var(name)
        raise RuntimeError(f"Undefined variable {name}.")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.var_values:
            self.var_values[name.lexeme] = value
        elif self.enclosing:
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError(name, f"Undefined variable '{name}'.")

    def ancestor(self, distance: int) -> "Environment":
        environment = self
        for _ in range(distance):
            if environment.enclosing is None:
                raise RuntimeError("No ancestor at the given distance")
            environment = environment.enclosing
        return environment

    def get_at(self, distance: int, name: str) -> Any:
        return self.ancestor(distance).var_values.get(name)

    def assign_at(self, distance: int, name: Token, value: Any) -> None:
        self.ancestor(distance).var_values[name.lexeme] = value
