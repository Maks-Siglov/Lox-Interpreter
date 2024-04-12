import expression
import stmt
from environment import Environment
from token_type import TokenType


class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements: list[stmt.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(error)

    def execute(self, statement: stmt.Stmt):
        statement.accept(self)

    def visit_expression_stmt(self, statement: stmt.Expression):
        self.evaluate(statement.expr)

    def visit_print_stmt(self, statement):
        value = self.evaluate(statement.expr)
        print(self.stringify(value))
        return None

    def visit_var_stmt(self, statement: stmt.Var):
        value = None
        if statement.initializer is not None:
            value = self.evaluate(statement.initializer)

        self.environment.define_var(statement.name.lexeme, value)

    def visit_var_expr(self, expr: expression.Var):
        return self.environment.get_var(expr.name)

    def visit_assign_expr(self, expr: expression.Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name.lexeme, value)
        return value

    @staticmethod
    def visit_literal_expr(expr: expression.Literal):
        return expr.value

    def visit_grouping_expr(self, expr: expression.Grouping):
        return self.evaluate(expr.expr)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        operator_type = expr.operator.token_type

        if operator_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif operator_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif operator_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif operator_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        elif operator_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif operator_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        elif operator_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)

        elif operator_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)

            raise RuntimeError(
                f"Operands must be two numbers or two strings."
                f" Operator: {operator_type}"
            )

        elif operator_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif operator_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        return None

    def evaluate(self, expr: expression.Expr):
        return expr.accept(self)

    @staticmethod
    def is_truthy(value) -> bool:
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

    @staticmethod
    def check_number_operand(operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(
            f"Operand must be a float number. Operator: {operator}"
        )

    @staticmethod
    def check_number_operands(operator, right, left):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(
            f"Operands must be a float number. Operator: {operator}"
        )

    @staticmethod
    def stringify(value):
        if value is None:
            return "nil"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)
