from typing import TYPE_CHECKING

import expr
import stmt

if TYPE_CHECKING:
    from interpreter import Interpreter


class Resolver:
    def __init__(self, interpreter: 'Interpreter'):
        self.interpreter = interpreter
        self.scopes = []

    def resolve(self, statements: list[stmt.Stmt]):
        for statement in statements:
            self.resolve_statement(statement)

    def resolve_statement(self, statement: stmt.Stmt):
        statement.accept(self)

    def begin_scope(self):
        hash_map: dict[str, bool] = {}
        self.scopes.append(hash_map)

    def end_scope(self):
        self.scopes.pop()

    def resolve_expression(self, expression: expr.Expr):
        expression.accept(self)

    def visit_block_stmt(self, block_stmt: stmt.Block):
        self.begin_scope()
        self.resolve(block_stmt.statements)
        self.end_scope()
