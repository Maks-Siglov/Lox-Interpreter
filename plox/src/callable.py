import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from interpreter import Interpreter


class PloxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> Any:
        pass


class ClockCallable(PloxCallable):
    def arity(self):
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> float:
        return time.time()

    def __str__(self):
        return "<native fn>"
