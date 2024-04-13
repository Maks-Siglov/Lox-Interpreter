import expr
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

    def visit_if_stmt(self, statement: stmt.IfStmt):
        if self.is_truthy(self.evaluate(statement.condition)):
            self.execute(statement.then_stmt)
        elif statement.else_stmt is not None:
            self.execute(statement.else_stmt)
        return None

    def visit_block_stmt(self, block_stmt: stmt.Block):
        self.execute_block(
            block_stmt.statements, Environment(enclosing=self.environment)
        )
        return None

    def execute_block(
        self, statements: list[stmt.Stmt], environment: Environment
    ):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_var_stmt(self, statement: stmt.Var):
        value = None
        if statement.initializer is not None:
            value = self.evaluate(statement.initializer)

        self.environment.define_var(statement.name.lexeme, value)

    def visit_while_stmt(self, statement: stmt.While):
        while self.is_truthy(statement.condition):
            self.execute(statement.body)

    def visit_var_expr(self, var_expr: expr.Var):
        return self.environment.get_var(var_expr.token.lexeme)

    def visit_assign_expr(self, assign_expr: expr.Assign):
        value = self.evaluate(assign_expr.value)
        self.environment.assign(assign_expr.name.lexeme, value)
        return value

    @staticmethod
    def visit_literal_expr(literal_expr: expr.Literal):
        return literal_expr.value

    def visit_logical_expr(self, logical_expr: expr.Logical):
        left = self.evaluate(logical_expr.left)

        if logical_expr.operator.token_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(logical_expr.right)

    def visit_grouping_expr(self, grouping_expr: expr.Grouping):
        return self.evaluate(grouping_expr.expr)

    def visit_unary_expr(self, unary_expr: expr.Unary):
        right = self.evaluate(unary_expr.right)
        if unary_expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        if unary_expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(unary_expr.operator, right)
            return -right

    def visit_binary_expr(self, binary_expr: expr.Binary):
        left = self.evaluate(binary_expr.left)
        right = self.evaluate(binary_expr.right)

        operator_type = binary_expr.operator.token_type

        if operator_type == TokenType.GREATER:
            self.check_number_operands(binary_expr.operator, left, right)
            return float(left) > float(right)
        elif operator_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(binary_expr.operator, left, right)
            return float(left) >= float(right)
        elif operator_type == TokenType.LESS:
            self.check_number_operands(binary_expr.operator, left, right)
            return float(left) < float(right)
        elif operator_type == TokenType.LESS_EQUAL:
            self.check_number_operands(binary_expr.operator, left, right)
            return float(left) <= float(right)

        elif operator_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif operator_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        elif operator_type == TokenType.MINUS:
            self.check_number_operands(binary_expr.operator, left, right)
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
            self.check_number_operands(binary_expr.operator, left, right)
            return float(left) / float(right)
        elif operator_type == TokenType.STAR:
            self.check_number_operands(binary_expr.operator, left, right)
            return float(left) * float(right)

        return None

    def evaluate(self, expression: expr.Expr):
        return expression.accept(self)

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
