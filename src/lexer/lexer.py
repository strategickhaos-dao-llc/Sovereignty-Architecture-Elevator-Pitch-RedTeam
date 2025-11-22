# src/lexer/lexer.py

class Token:
    def __init__(self, type_, lexeme, literal, line):
        self.type = type_          # e.g. "PRINT", "NUMBER", "PLUS"
        self.lexeme = lexeme       # raw text from source
        self.literal = literal     # parsed value (for NUMBER, etc.)
        self.line = line

    def __repr__(self):
        return f"{self.type} {self.lexeme} {self.literal}"


KEYWORDS = {
    "let": "LET",
    "print": "PRINT",
    "show": "SHOW",
    "fn": "FN",
    "return": "RETURN",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "true": "TRUE",
    "false": "FALSE",
    "nil": "NIL",
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        if c == '(':
            self.add_token("LEFT_PAREN")
        elif c == ')':
            self.add_token("RIGHT_PAREN")
        elif c == '{':
            self.add_token("LEFT_BRACE")
        elif c == '}':
            self.add_token("RIGHT_BRACE")
        elif c == ',':
            self.add_token("COMMA")
        elif c == '.':
            self.add_token("DOT")
        elif c == '-':
            self.add_token("MINUS")
        elif c == '+':
            self.add_token("PLUS")
        elif c == ';':
            self.add_token("SEMICOLON")
        elif c == '*':
            self.add_token("STAR")
        elif c == '!':
            self.add_token("BANG")
        elif c == '=':
            self.add_token("EQUAL")
        elif c == '<':
            self.add_token("LESS")
        elif c == '>':
            self.add_token("GREATER")
        elif c == '/':
            if self.match('/'):
                # comment until end of line
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token("SLASH")
        elif c in (' ', '\r', '\t'):
            # ignore whitespace
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        elif c == 'λ':
            self.add_token("LAMBDA")
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == '_':
            self.identifier()
        else:
            raise SyntaxError(f"[line {self.line}] Unexpected character: {c}")

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            raise SyntaxError(f"[line {self.line}] Unterminated string.")
        # closing "
        self.advance()
        # keep quotes in lexeme, but literal is the inside
        text = self.source[self.start:self.current]
        value = text[1:-1]
        self.add_token("STRING", value)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        text = self.source[self.start:self.current]
        literal = float(text)
        self.add_token("NUMBER", literal)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        type_ = KEYWORDS.get(text, "IDENTIFIER")
        self.add_token(type_)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        ch = self.source[self.current]
        self.current += 1
        return ch

    def add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))
