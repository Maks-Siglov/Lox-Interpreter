import stmt
from expression import Binary, Expr, Grouping, Literal, Unary, Var, Assign
from plox_token import Token
from stmt import Expression, Print, Stmt, Block, IfStmt
from token_type import TokenType


class ParserError(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def declaration(self):
        if self.match([TokenType.VAR]):
            return self.var_declaration()
        return self.statement()

    def var_declaration(self):
        token = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match([TokenType.EQUAL]):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Var(token, initializer)

    def statement(self) -> Stmt:
        if self.match([TokenType.PRINT]):
            return self.print_statement()
        elif self.match([TokenType.LEFT_BRACE]):
            return self.block_statement()
        elif self.match([TokenType.IF]):
            return self.if_statement()
        return self.expression_statement()

    def print_statement(self) -> Print:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def block_statement(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return Block(statements)

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after 'if'.")

        then_branch = self.statement()
        else_branch = None
        if self.match([TokenType.ELSE]):
            else_branch = self.statement()

        return IfStmt(condition, then_branch, else_branch)

    def expression_statement(self) -> Expression:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(expr)

    def expression(self) -> Expr:
        return self.assigment()

    def assigment(self) -> Expr:
        expr = self.equality()

        if self.match([TokenType.EQUAL]):
            value = self.assigment()

            if isinstance(expr, Var):
                token = expr.token
                return Assign(token, value)

            raise ParserError(f"Invalid assigment target: {type(expr)}")

        return expr

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        comparison_types = [
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ]

        while self.match(comparison_types):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match([TokenType.FALSE]):
            return Literal(False)
        elif self.match([TokenType.TRUE]):
            return Literal(True)
        elif self.match([TokenType.NIL]):
            return Literal(None)

        elif self.match([TokenType.STRING, TokenType.NUMBER]):
            return Literal(self.previous().literal)

        elif self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        elif self.match([TokenType.IDENTIFIER]):
            return Var(self.previous())

        self.error(self.peek(), "Expect expression.")

    def consume(
        self, token_type: TokenType, message: str
    ) -> Token | ParserError:
        if self.check(token_type):
            return self.advance()

        self.error(self.peek(), message)

    def match(self, types: list[TokenType]) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def check(self, expected_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == expected_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    @staticmethod
    def error(token: Token, message: str):
        msg = f"Error: {message}, token: {token}"
        raise ParserError(msg)

    def synchronize(self) -> None:
        self.advance()

        keywords = [
            TokenType.CLASS,
            TokenType.FUN,
            TokenType.VAR,
            TokenType.FOR,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.PRINT,
            TokenType.RETURN,
        ]

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            next_type = self.peek().token_type
            if next_type in keywords:
                return

            self.advance()
