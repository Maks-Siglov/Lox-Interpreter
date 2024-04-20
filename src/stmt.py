from expr import Expr
from plox_token import Token


class Stmt:
    """
    Program -> Declaration * EOF ;
    Declaration -> VarDecl | Statement :
    VarDecl -> "var" IDENTIFIER ( "=" expression )? ";" ;
    Statement -> ExprStmt | PrintStmt | Block | ifStmt | WhileStmt | ForStmt ;
    ifStmt -> "if" "(" expression ")" statement
        ( "else" statement )? ;
    WhileStmt -> "while" "(" expression ")" statement ;
    ForStmt -> "for" "("
        ( varDecl | exprStmt | ";" ) expression? ";" expression?
        )" statement ;
    Block -> "{" Declaration* "}" ;
    ExprStmt -> expression ";" ;
    PrintStmt -> "print" expression ";" ;
    """

    def accept(self, visitor):
        raise NotImplementedError(
            "accept method must be implemented by Stmt subclasses"
        )


class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)


class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


class IfStmt(Stmt):
    def __init__(self, condition: Expr, then_stmt: Stmt, else_stmt: Stmt):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    def accept(self, visitor):
        return visitor.self_if_stmt(self)


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)
