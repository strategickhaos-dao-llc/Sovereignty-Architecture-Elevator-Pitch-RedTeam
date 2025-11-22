class ParseError(Exception):
    pass


class Stmt:
    def __init__(self, type_, **kwargs):
        self.type = type_
        for key, value in kwargs.items():
            setattr(self, key, value)


class Expr:
    def __init__(self, type_, **kwargs):
        self.type = type_
        for key, value in kwargs.items():
            setattr(self, key, value)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.match("PRINT", "SHOW"):
            expr = self.expression()
            self.consume("SEMICOLON", "Expect ';' after statement.")
            return Stmt("PRINT", expression=expr)
        if self.match("LET"):
            name = self.consume("IDENTIFIER", "Expect variable name.")
            self.consume("EQUAL", "Expect '=' after let.")
            expr = self.expression()
            self.consume("SEMICOLON", "Expect ';' after let.")
            return Stmt("LET", name=name, expression=expr)
        raise ParseError("Expected statement.")

    def expression(self):
        return self.addition()

    def addition(self):
        expr = self.multiplication()
        while self.match("PLUS", "MINUS"):
            operator = self.previous()
            right = self.multiplication()
            expr = Expr("BINARY", left=expr, operator=operator, right=right)
        return expr

    def multiplication(self):
        expr = self.unary()
        while self.match("STAR", "SLASH"):
            operator = self.previous()
            right = self.unary()
            expr = Expr("BINARY", left=expr, operator=operator, right=right)
        return expr

    def unary(self):
        if self.match("MINUS"):
            operator = self.previous()
            right = self.unary()
            return Expr("UNARY", operator=operator, right=right)
        return self.primary()

    def primary(self):
        if self.match("NUMBER"):
            return Expr("LITERAL", value=self.previous().literal)
        if self.match("STRING"):
            return Expr("LITERAL", value=self.previous().literal)
        if self.match("IDENTIFIER"):
            return Expr("VARIABLE", name=self.previous())
        if self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after expression.")
            return Expr("GROUPING", expression=expr)
        raise ParseError(f"Unexpected token {self.peek()}")

    # Helper methods
    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, type_, message):
        if self.check(type_):
            return self.advance()
        raise ParseError(message)

    def check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
