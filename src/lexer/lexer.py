class Token:
    def __init__(self, type_, lexeme, literal=None, line=1):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme}, {self.literal})"


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            "let": "LET",
            "print": "PRINT",
            "show": "SHOW",
            "if": "IF",
            "else": "ELSE",
            "while": "WHILE",
            "for": "FOR",
            "return": "RETURN",
            "true": "TRUE",
            "false": "FALSE",
            "nil": "NIL",
            "and": "AND",
            "or": "OR",
            "not": "NOT",
        }

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        if c == "(":
            self.add_token("LEFT_PAREN")
        elif c == ")":
            self.add_token("RIGHT_PAREN")
        elif c == "{":
            self.add_token("LEFT_BRACE")
        elif c == "}":
            self.add_token("RIGHT_BRACE")
        elif c == "[":
            self.add_token("LEFT_BRACKET")
        elif c == "]":
            self.add_token("RIGHT_BRACKET")
        elif c == ",":
            self.add_token("COMMA")
        elif c == ".":
            self.add_token("DOT")
        elif c == "-":
            self.add_token("MINUS")
        elif c == "+":
            self.add_token("PLUS")
        elif c == ";":
            self.add_token("SEMICOLON")
        elif c == "*":
            self.add_token("STAR")
        elif c == "!":
            self.add_token("BANG_EQUAL" if self.match("=") else "BANG")
        elif c == "=":
            self.add_token("EQUAL_EQUAL" if self.match("=") else "EQUAL")
        elif c == "<":
            self.add_token("LESS_EQUAL" if self.match("=") else "LESS")
        elif c == ">":
            self.add_token("GREATER_EQUAL" if self.match("=") else "GREATER")
        elif c == "/":
            if self.match("/"):
                # Comment goes to end of line
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token("SLASH")
        elif c in [" ", "\r", "\t"]:
            # Ignore whitespace
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                # Unknown character, skip
                pass

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        type_ = self.keywords.get(text, "IDENTIFIER")
        self.add_token(type_)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Look for decimal part
        if self.peek() == "." and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token("NUMBER", float(self.source[self.start : self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            # Unterminated string
            return

        # Closing "
        self.advance()

        # Trim surrounding quotes
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token("STRING", value)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_alpha(self, c):
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c):
        return c >= "0" and c <= "9"

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type_, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type_, text, literal, self.line))
