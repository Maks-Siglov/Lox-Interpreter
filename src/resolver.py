from typing import TYPE_CHECKING

import expr
import stmt
from exceptions import ResolveError
from plox_token import Token

if TYPE_CHECKING:
    from interpreter import Interpreter


class Resolver:
    def __init__(self, interpreter: "Interpreter"):
        self.interpreter = interpreter
        self.scopes = []

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
            scope[name.lexeme] = False

    def define(self, name: Token):
        if self.scopes:
            self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expression, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expression, len(self.scopes) - 1 - i)
                return

    def resolve_function(self, function_stmt: stmt.Function):
        self.begin_scope()
        for param in function_stmt.params:
            self.declare(param)
            self.define(param)

        self.resolve(function_stmt.body)
        self.end_scope()

    def visit_block_stmt(self, block_stmt: stmt.Block):
        self.begin_scope()
        self.resolve(block_stmt.statements)
        self.end_scope()

    def visit_var_stmt(self, var_stmt: stmt.Var):
        self.declare(var_stmt.name)
        if not var_stmt.initializer is None:
            self.resolve_expression(var_stmt.initializer)

        self.define(var_stmt.name)

    def visit_function_stmt(self, function_stmt: stmt.Function):
        self.declare(function_stmt.name)
        self.define(function_stmt.name)

        self.resolve_function(function_stmt)

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

    @staticmethod
    def error(token: Token, message: str):
        msg = f"Error: {message}, token: {token}"
        raise ResolveError(msg)
