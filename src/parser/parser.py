# src/parser/parser.py

class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    # ===== ENTRY =====

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    # ===== DECLARATIONS =====

    def declaration(self):
        try:
            if self.match("FN"):
                return self.function("function")
            return self.statement()
        except ParseError:
            # simple panic mode: skip token
            self.advance()
            return None

    def function(self, kind):
        name = self.consume("IDENTIFIER", f"Expect {kind} name.")
        self.consume("LEFT_PAREN", "Expect '(' after function name.")
        params = []
        if not self.check("RIGHT_PAREN"):
            while True:
                params.append(self.consume("IDENTIFIER", "Expect parameter name."))
                if not self.match("COMMA"):
                    break
        self.consume("RIGHT_PAREN", "Expect ')' after parameters.")
        self.consume("LEFT_BRACE", f"Expect '{{' before {kind} body.")
        body = self.block()
        return {"type": "FUNCTION", "name": name, "params": params, "body": body}

    # ===== STATEMENTS =====

    def statement(self):
        if self.match("PRINT", "SHOW"):
            expr = self.expression()
            self.consume("SEMICOLON", "Expect ';' after print statement.")
            return {"type": "PRINT", "expression": expr}

        if self.match("LET"):
            name = self.consume("IDENTIFIER", "Expect variable name.")
            self.consume("EQUAL", "Expect '=' after let.")
            expr = self.expression()
            self.consume("SEMICOLON", "Expect ';' after let.")
            return {"type": "LET", "name": name, "expression": expr}

        if self.match("RETURN"):
            value = None
            if not self.check("SEMICOLON"):
                value = self.expression()
            self.consume("SEMICOLON", "Expect ';' after return value.")
            return {"type": "RETURN", "expression": value}

        if self.match("IF"):
            self.consume("LEFT_PAREN", "Expect '(' after 'if'.")
            cond = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after condition.")
            then_branch = self.statement()
            else_branch = None
            if self.match("ELSE"):
                else_branch = self.statement()
            return {"type": "IF", "condition": cond, "then": then_branch, "else": else_branch}

        if self.match("WHILE"):
            self.consume("LEFT_PAREN", "Expect '(' after 'while'.")
            cond = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after condition.")
            body = self.statement()
            return {"type": "WHILE", "condition": cond, "body": body}

        if self.match("LEFT_BRACE"):
            return {"type": "BLOCK", "statements": self.block()}

        # Expression statement
        expr = self.expression()
        self.consume("SEMICOLON", "Expect ';' after expression.")
        return {"type": "EXPR_STMT", "expression": expr}

    def block(self):
        statements = []
        while not self.check("RIGHT_BRACE") and not self.is_at_end():
            statements.append(self.declaration())
        self.consume("RIGHT_BRACE", "Expect '}' after block.")
        return statements

    # ===== EXPRESSIONS =====

    def expression(self):
        return self.addition()  # simple for now; could expand to equality/comparison

    def addition(self):
        expr = self.multiplication()
        while self.match("PLUS", "MINUS"):
            operator = self.previous()
            right = self.multiplication()
            expr = {"type": "BINARY", "left": expr, "operator": operator, "right": right}
        return expr

    def multiplication(self):
        expr = self.unary()
        while self.match("STAR", "SLASH"):
            operator = self.previous()
            right = self.unary()
            expr = {"type": "BINARY", "left": expr, "operator": operator, "right": right}
        return expr

    def unary(self):
        if self.match("MINUS"):
            operator = self.previous()
            right = self.unary()
            return {"type": "UNARY", "operator": operator, "right": right}
        return self.call()

    def call(self):
        expr = self.primary()
        while True:
            if self.match("LEFT_PAREN"):
                args = []
                if not self.check("RIGHT_PAREN"):
                    while True:
                        args.append(self.expression())
                        if not self.match("COMMA"):
                            break
                self.consume("RIGHT_PAREN", "Expect ')' after arguments.")
                expr = {"type": "CALL", "callee": expr, "arguments": args}
            else:
                break
        return expr

    def primary(self):
        if self.match("NUMBER"):
            tok = self.previous()
            return {"type": "LITERAL", "value": tok.literal}

        if self.match("STRING"):
            tok = self.previous()
            return {"type": "LITERAL", "value": tok.literal}

        if self.match("TRUE"):
            return {"type": "LITERAL", "value": True}
        if self.match("FALSE"):
            return {"type": "LITERAL", "value": False}
        if self.match("NIL"):
            return {"type": "LITERAL", "value": None}

        if self.match("IDENTIFIER"):
            return {"type": "VARIABLE", "name": self.previous()}

        if self.match("LAMBDA"):
            return self.lambda_expr()

        if self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after expression.")
            return {"type": "GROUPING", "expression": expr}

        raise ParseError(f"Unexpected token {self.peek().type}")

    def lambda_expr(self):
        # λ(params) { body }
        self.consume("LEFT_PAREN", "Expect '(' after λ.")
        params = []
        if not self.check("RIGHT_PAREN"):
            while True:
                params.append(self.consume("IDENTIFIER", "Expect parameter name in lambda."))
                if not self.match("COMMA"):
                    break
        self.consume("RIGHT_PAREN", "Expect ')' after lambda parameters.")
        self.consume("LEFT_BRACE", "Expect '{' before lambda body.")
        body = self.block()
        return {"type": "LAMBDA", "params": params, "body": body}

    # ===== UTILITIES =====

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
