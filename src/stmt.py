class Stmt:
    """
    Program -> Declaration * EOF ;
    Declaration -> VarDecl | Statement :
    VarDecl -> "var" IDENTIFIER ( "=" expression )? ";" ;
    Statement -> ExprStmt | PrintStmt | Block | ifStmt | WhileStmt;
    ifStmt -> "if" "(" expression ")" statement
        ( "else" statement )? ;
    WhileStmt -> "while" "(" expression ")" statement ;
    Block -> "{" Declaration* "}" ;
    ExprStmt -> expression ";" ;
    PrintStmt -> "print" expression ";" ;
    """

    def accept(self, visitor):
        raise NotImplementedError(
            "accept method must be implemented by Expr subclasses"
        )


class Print(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)


class Expression(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)


class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


class IfStmt(Stmt):
    def __init__(self, condition, then_stmt, else_stmt):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    def accept(self, visitor):
        return visitor.self_if_stmt(self)


class While(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)
