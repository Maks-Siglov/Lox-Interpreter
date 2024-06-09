import typing as t

from token_type import TokenType


class Token:
    def __init__(
        self,
        token_type: TokenType,
        lexeme: str,
        literal: t.Any,
        line: int,
    ):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"
