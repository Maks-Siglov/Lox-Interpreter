from expression import Binary
from token_type import TokenType


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
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

    def term(self):
        expr = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        pass

    def match(self, types):
        for token_type in types:
            if self.check(token_type):
                return True

        return False

    def check(self, expected_type):
        if self.is_at_end():
            return False
        return self.peek().type == expected_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self):
        return self.tokens.get(self.current)

    def previous(self):
        return self.tokens.get(self.current - 1)

    def is_at_end(self):
        return self.peek().type == "EOF"
