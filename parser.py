from expression import (
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary,
)
from plox_token import Token
from token_type import TokenType


class ParserError(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParserError as e:
            print(e)
            return None

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        comparison_types = [
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ]

        while self.match(comparison_types):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match([TokenType.FALSE]):
            return Literal(False)
        elif self.match([TokenType.TRUE]):
            return Literal(True)
        elif self.match([TokenType.NIL]):
            return Literal(None)

        elif self.match([TokenType.STRING, TokenType.NUMBER]):
            return Literal(self.previous().literal)

        elif self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.LEFT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        self.error(self.peek(), "Expect expression.")

    def consume(
        self, token_type: TokenType, message: str
    ) -> Token | ParserError:
        if self.check(token_type):
            return self.advance()

        # self.error(self.peek(), message)

    def match(self, types: list[TokenType]) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def check(self, expected_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == expected_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().token_type == "EOF"

    @staticmethod
    def error(token: Token, message: str):
        msg = f"Error: {message}, token: {token}"
        raise ParserError(msg)

    def synchronize(self) -> None:
        self.advance()

        keywords = [
            TokenType.CLASS,
            TokenType.FUN,
            TokenType.VAR,
            TokenType.FOR,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.PRINT,
            TokenType.RETURN,
        ]

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            next_type = self.peek().token_type
            if next_type in keywords:
                return

            self.advance()
