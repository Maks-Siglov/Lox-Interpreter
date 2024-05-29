import expr
import stmt
from callable import ClockCallable, PloxCallable
from environment import Environment
from exceptions import ReturnError
from plox_class import LoxClass
from plox_function import LoxFunction
from plox_instance import LoxInstance
from plox_token import Token
from token_type import TokenType


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals: dict[expr, int] = {}

        self.globals.define_var("clock", ClockCallable())

    def interpret(self, statements: list[stmt.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(error)

    def execute(self, statement: stmt.Stmt):
        statement.accept(self)

    def resolve(self, expression: expr.Expr, depth: int):
        self.locals[expression] = depth

    def look_up_var(self, name: Token, var_expr: expr.Var | expr.Self):
        distance = self.locals.get(var_expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        return self.globals.get_var(name)

    def visit_expression_stmt(self, statement: stmt.Expression):
        self.evaluate(statement.expr)

    def visit_function_stmt(self, statement: stmt.Function):
        function = LoxFunction(statement, self.environment, False)
        self.environment.define_var(statement.name.lexeme, function)

    def visit_class_stmt(self, statement: stmt.Class):
        superclass = None
        if statement.superclass is not None:
            superclass = self.evaluate(statement.superclass)
            if not isinstance(superclass, LoxClass):
                raise RuntimeError(
                    statement.superclass.token, "Superclass must be a class."
                )

        self.environment.define_var(statement.name.lexeme, None)

        if statement.superclass is not None:
            self.environment = Environment(enclosing=self.environment)
            self.environment.define_var("super", superclass)

        methods = {}
        for method in statement.methods:
            is_init: bool = method.name.lexeme == "init"
            function = LoxFunction(method, self.environment, is_init)
            methods[method.name.lexeme] = function

        klass = LoxClass(statement.name.lexeme, superclass, methods)

        if statement.superclass is not None:
            self.environment = self.environment.enclosing

        self.environment.assign(statement.name, klass)

    def visit_print_stmt(self, statement: stmt.Print):
        value = self.evaluate(statement.expr)
        print(self.stringify(value))
        return None

    def visit_return_stmt(self, statement: stmt.Return):
        value = None
        if statement.value is not None:
            value = self.evaluate(statement.value)

        raise ReturnError(value)

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
        while self.evaluate(statement.condition):
            self.execute(statement.body)

    def visit_var_expr(self, var_expr: expr.Var):
        return self.look_up_var(var_expr.token, var_expr)
        # return self.environment.get_var(var_expr.token.lexeme)

    def visit_assign_expr(self, assign_expr: expr.Assign):
        value = self.evaluate(assign_expr.value)
        # self.environment.assign(assign_expr.name.lexeme, value)

        distance = self.locals[assign_expr]
        if distance is not None:
            self.environment.assign_at(distance, assign_expr.name, value)
        else:
            self.globals.assign(assign_expr.name, value)

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

    def visit_call_expr(self, call_expr: expr.Call):
        calle = self.evaluate(call_expr.calle)

        arguments = []
        for argument in call_expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(calle, PloxCallable):
            raise RuntimeError("Can only call functions and classes.")

        function: PloxCallable = calle

        if len(arguments) != function.arity():
            raise RuntimeError(
                f"Expected {function.arity()} arguments, "
                f"but {len(arguments)} were given."
            )
        return function.call(self, arguments)

    def visit_get_expr(self, get_expr: expr.Get):
        obj = self.evaluate(get_expr.expression)
        if isinstance(obj, LoxInstance):
            return obj.get(get_expr.name)
        raise RuntimeError(obj.name, "Only instances have properties.")

    def visit_set_expr(self, set_expr: expr.Set):
        obj = self.evaluate(set_expr.expression)

        if not isinstance(obj, LoxInstance):
            RuntimeError(set_expr.name, "Only instances have fields.")

        value = self.evaluate(set_expr.value)
        obj.set(set_expr.name, value)
        return value

    def visit_super_expr(self, super_expr: expr.Super):
        distance = self.locals.get(super_expr)
        superclass: LoxClass = self.environment.get_at(distance, "super")
        instance = self.environment.get_at(distance - 1, "self")

        method = superclass.get_method(super_expr.method.lexeme)
        if method is None:
            raise RuntimeError(
                super_expr.method,
                f"Undefined property: '{super_expr.method.lexeme}'."
            )
        return method.bind(instance)

    def visit_self_expr(self, self_expr: expr.Self):
        return self.look_up_var(self_expr.keyword, self_expr)

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
