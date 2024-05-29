import expr
from expr import Expr
from plox_token import Token


class Stmt:
    """
    Program -> Declaration * EOF ;
    Declaration -> VarDecl
                    | Statement
                    | FunDecl
                    | ClassDecl ;
    VarDecl -> "var" IDENTIFIER ( "=" expression )? ";" ;
    FunDecl -> "fun" Function ;
    Function → IDENTIFIER "(" Parameters? ")" block ;
    ClassDecl -> "class" IDENTIFIER ( "<" IDENTIFIER )? {" function* "}" ;
    Parameters → IDENTIFIER ( "," IDENTIFIER )* ;
    Statement -> ExprStmt
                | PrintStmt
                | Block
                | ifStmt
                | WhileStmt
                | ForStmt
                | ReturnStmt ;
    ifStmt -> "if" "(" expression ")" statement ( "else" statement )? ;
    WhileStmt -> "while" "(" expression ")" statement ;
    ForStmt -> "for" "("
        ( varDecl | exprStmt | ";" ) expression? ";" expression?
        )" statement ;
    ReturnStmt -> "return" expression? ";" ;
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
        return visitor.visit_if_stmt(self)


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


class Function(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)


class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


class Class(Stmt):
    def __init__(
            self,
            name: Token,
            superclass: expr.Var | None,
            methods: list[Function]
    ):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor):
        return visitor.visit_class_stmt(self)
