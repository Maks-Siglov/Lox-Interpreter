from expression import Grouping, Literal, Expr
from token_type import TokenType


class Interpreter:
    @staticmethod
    def visit_literal_expr(expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        if expr.operator.token_type == TokenType.MINUS:
            return -right

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        operator_type = expr.operator.type

        if operator_type == TokenType.GREATER:
            return float(left) > float(right)
        elif operator_type == TokenType.GREATER_EQUAL:
            return float(left) >= float(right)
        elif operator_type == TokenType.LESS:
            return float(left) < float(right)
        elif operator_type == TokenType.LESS_EQUAL:
            return float(left) <= float(right)

        elif operator_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif operator_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        elif operator_type == TokenType.MINUS:
            return float(left) - float(right)

        elif operator_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)

        elif operator_type == TokenType.SLASH:
            return float(left) / float(right)
        elif operator_type == TokenType.STAR:
            return float(left) * float(right)

        return None

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    @staticmethod
    def is_truthy(value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    @staticmethod
    def is_equal(a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b
