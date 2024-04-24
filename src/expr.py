from typing import Any

from plox_token import Token


class Expr:
    """
    Expression -> Assignment ;
    assignment -> ( Call ".")? IDENTIFIER "=" Assignment | Equality ;
    Logic_or → Logic_and ( "or" Logic_and )* ;
    Logic_and → Equality ( "and" Equality )* ;
    Equality -> Comparison ( ( "!=" | "==" ) Comparison )* ;
    Comparison → Term ( ( ">" | ">=" | "<" | "<=" ) Term )* ;
    Term → Factor ( ( "-" | "+" ) Factor )* ;
    Factor → Unary ( ( "/" | "*" ) Unary )* ;
    Unary -> ("!" | "-")Unary | Primary;
    Call -> Primary ( "(" arguments? ")" | "." IDENTIFIER )* ;
    Primary -> "true" | "false" | "nil"
        |  NUMBER | STRING
        | "(" expression ")"
        | IDENTIFIER ;
    """

    def accept(self, visitor):
        raise NotImplementedError(
            "accept method must be implemented by Expr subclasses"
        )


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


class Var(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_var_expr(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)


class Call(Expr):
    def __init__(self, calle: Expr, paren: Token, arguments: list[Expr]):
        self.calle = calle
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)


class Get(Expr):
    def __init__(self, expression: Expr, name: Token):
        self.expression = expression
        self.name = name

    def accept(self, visitor):
        return visitor.visit_get_expr(self)


class Set(Expr):
    def __init__(self, expression: Expr, name: Token, value: Expr):
        self.expression = expression
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_set_expr(self)


class Self(Expr):
    def __init__(self, keyword: Token):
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visit_self_expr(self)
