from plox_token import Token


class Expr:
    """
    Expression -> Assignment ;
    assignment -> IDENTIFIER "=" Assignment | Equality ;
    Equality -> Comparison ( ( "!=" | "==" ) Comparison )* ;
    Comparison → Term ( ( ">" | ">=" | "<" | "<=" ) Term )* ;
    Term → Factor ( ( "-" | "+" ) Factor )* ;
    Factor → Unary ( ( "/" | "*" ) Unary )* ;
    Unary -> ("!" | "-")Unary | Primary;
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
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


class Var(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_var_expr(self)
