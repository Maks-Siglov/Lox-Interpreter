class Expr:
    """
    Expression -> Equality ;
    Equality -> Comparison ( ( "!=" | "==" ) Comparison )* ;
    Comparison → Term ( ( ">" | ">=" | "<" | "<=" ) Term )* ;
    Term → Factor ( ( "-" | "+" ) Factor )* ;
    Factor → Unary ( ( "/" | "*" ) Unary )* ;
    Unary -> ("!" | "-")Unary | Primary;
    Primary -> NUMBER | STRING | "true" | "false" | "nil"
        | "(" expression ")" ;
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
