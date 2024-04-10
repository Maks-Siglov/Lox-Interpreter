from token import Token
from token_type import TokenType


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(
            Token(
                token_type=TokenType.EOF,
                lexeme="",
                literal=None,
                line=self.line,
            )
        )
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type, literal=None):
        text = self.source[self.start: self.current]
        self.tokens.append(
            Token(
                token_type=token_type,
                lexeme=text,
                literal=literal,
                line=self.line,
            )
        )

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "/0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "/0"
        return self.source[self.current + 1]

    def scan_token(self):
        c = self.advance()
        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            token_type = (
                TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
            )
            self.add_token(token_type)
        elif c == "=":
            token_type = (
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            )
            self.add_token(token_type)
        elif c == "<":
            token_type = (
                TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
            )
            self.add_token(token_type)
        elif c == ">":
            token_type = (
                TokenType.GREATER_EQUAL
                if self.match("=")
                else TokenType.GREATER
            )
            self.add_token(token_type)

        elif c == "/":
            if self.match("/"):
                # Comment goes until the end of the line
                # We don't call add_token(), because comments aren't meaningful
                while self.peek() != "/n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)

        elif c in [" ", "/r", "/t"]:
            # Ignore whitespace
            pass

        elif c == "/n":
            self.line += 1

        elif c == '"':
            self.string()

        elif c.isdigit():
            self.number()

        elif c.isalpha():
            self.identifier()

        else:
            # Lox.error(self.line, f"Unexpected character: {c}")
            print(f"Unexpected character: {c}. Line: {self.line}")

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "/n":
                self.line += 1

            self.advance()

        if self.is_at_end():
            print(f"Unterminated string. Line: {self.line}")
            return

        self.advance()
        string_value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, literal=string_value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            # Skip '.'
            self.advance()

            while self.peek().isdigit():
                self.advance()

        self.add_token(
            TokenType.NUMBER,
            literal=float(self.source[self.start: self.current]),
        )

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        # Check if identifier is a reserved keyword
        text = self.source[self.start: self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)

        self.add_token(token_type=token_type)
