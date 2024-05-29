from typing import TYPE_CHECKING

import expr
import stmt
from exceptions import ResolveError
from plox_class import ClassType
from plox_function import FunctionType
from plox_token import Token

if TYPE_CHECKING:
    from interpreter import Interpreter


class Resolver:
    def __init__(self, interpreter: "Interpreter"):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def resolve(self, statements: list[stmt.Stmt]):
        for statement in statements:
            self.resolve_statement(statement)

    def resolve_statement(self, statement: stmt.Stmt):
        statement.accept(self)

    def resolve_expression(self, expression: expr.Expr):
        expression.accept(self)

    def begin_scope(self):
        hash_map: dict[str, bool] = {}
        self.scopes.append(hash_map)

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if self.scopes:
            scope = self.scopes[-1]

            if name.lexeme in scope:
                self.error(
                    name, "Already variable with this name in this scope."
                )

            scope[name.lexeme] = False

    def define(self, name: Token):
        if self.scopes:
            self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expression, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expression, len(self.scopes) - 1 - i)
                return

    def resolve_function(
        self, function_stmt: stmt.Function, func_type: FunctionType
    ):
        enclosing_function = self.current_function
        self.current_function = func_type
        self.begin_scope()

        for param in function_stmt.params:
            self.declare(param)
            self.define(param)

        self.resolve(function_stmt.body)
        self.end_scope()
        self.current_function = enclosing_function

    def visit_block_stmt(self, block_stmt: stmt.Block):
        self.begin_scope()
        self.resolve(block_stmt.statements)
        self.end_scope()

    def visit_var_stmt(self, var_stmt: stmt.Var):
        self.declare(var_stmt.name)
        if var_stmt.initializer is not None:
            self.resolve_expression(var_stmt.initializer)

        self.define(var_stmt.name)

    def visit_function_stmt(self, function_stmt: stmt.Function):
        self.declare(function_stmt.name)
        self.define(function_stmt.name)

        self.resolve_function(function_stmt, FunctionType.FUNCTION)

    def visit_class_stmt(self, class_stmt: stmt.Class) -> None:
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS

        self.declare(class_stmt.name)
        self.define(class_stmt.name)

        if class_stmt.superclass is not None:
            if class_stmt.name.lexeme == class_stmt.superclass.token.lexeme:
                self.error(
                    class_stmt.superclass.token,
                    "A class can't inherit from itself."
                )

            self.resolve_expression(class_stmt.superclass)

        self.begin_scope()
        self.scopes[-1]["self"] = True

        for method in class_stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER

            self.resolve_function(method, declaration)

        self.current_class = enclosing_class

        self.end_scope()

    def visit_var_expr(self, expression: expr.Var):
        if (
            self.scopes
            and self.scopes[-1].get(expression.token.lexeme) is False
        ):
            self.error(
                expression.token,
                "Can't read local variable in its own initializer.",
            )
        self.resolve_local(expression, expression.token)

    def visit_assign_expr(self, assign_expr: expr.Assign):
        self.resolve_expression(assign_expr.value)
        self.resolve_local(assign_expr, assign_expr.name)

    def visit_expression_stmt(self, expression_stmt: stmt.Expression):
        self.resolve_expression(expression_stmt.expr)

    def visit_if_stmt(self, if_stmt: stmt.IfStmt):
        self.resolve_expression(if_stmt.condition)
        self.resolve_statement(if_stmt.then_stmt)
        if if_stmt.else_stmt is not None:
            self.resolve_statement(if_stmt.else_stmt)

    def visit_print_stmt(self, print_stmt: stmt.Print):
        self.resolve_expression(print_stmt.expr)

    def visit_return_stmt(self, return_stmt: stmt.Return):
        if self.current_function == FunctionType.NONE:
            self.error(
                return_stmt.keyword, "Can't return from top-level code."
            )
        elif self.current_function == FunctionType.INITIALIZER:
            self.error(return_stmt.keyword, "Can't return from initializer.")

        if return_stmt.value is not None:
            self.resolve_expression(return_stmt.value)

    def visit_while_stmt(self, while_stmt: stmt.While):
        self.resolve_expression(while_stmt.condition)
        self.resolve_statement(while_stmt.body)

    def visit_binary_expr(self, binary_expr: expr.Binary):
        self.resolve_expression(binary_expr.left)
        self.resolve_expression(binary_expr.right)

    def visit_call_expr(self, call_expr: expr.Call):
        self.resolve_expression(call_expr.calle)

        for argument in call_expr.arguments:
            self.resolve_expression(argument)

    def visit_get_expr(self, get_expr: expr.Get):
        self.resolve_expression(get_expr.expression)

    def visit_set_expr(self, set_expr: expr.Set):
        self.resolve_expression(set_expr.value)
        self.resolve_expression(set_expr.expression)

    def visit_self_expr(self, self_expr: expr.Self) -> None:
        if self.current_class is ClassType.NONE:
            self.error(
                self_expr.keyword, "Can't use 'self' outside of a class."
            )
        self.resolve_local(self_expr, self_expr.keyword)

    def visit_grouping_expr(self, grouping_expr: expr.Grouping):
        self.resolve_expression(grouping_expr.expr)

    def visit_literal_expr(self, literal_expr: expr.Literal):
        return

    def visit_logical_expr(self, logical_expr: expr.Logical):
        self.resolve_expression(logical_expr.left)
        self.resolve_expression(logical_expr.right)

    def visit_unary_expr(self, unary_expr: expr.Unary):
        self.resolve_expression(unary_expr.right)

    @staticmethod
    def error(token: Token, message: str):
        msg = f"Error: {message}, token: {token}"
        raise ResolveError(msg)
