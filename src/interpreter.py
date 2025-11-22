class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, stmts):
        for stmt in stmts:
            self.execute(stmt)

    def execute(self, stmt):
        if stmt.type == "PRINT":
            value = self.evaluate(stmt.expression)
            print(value)
        elif stmt.type == "LET":
            value = self.evaluate(stmt.expression) if stmt.expression else None
            self.variables[stmt.name.lexeme] = value

    def evaluate(self, expr):
        if expr.type == "LITERAL":
            return expr.value
        elif expr.type == "BINARY":
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            op = expr.operator.type

            if op == "PLUS":
                return left + right
            if op == "MINUS":
                return left - right
            if op == "STAR":
                return left * right
            if op == "SLASH":
                return left / right
        elif expr.type == "GROUPING":
            return self.evaluate(expr.expression)
        elif expr.type == "VARIABLE":
            return self.variables.get(expr.name.lexeme)
        elif expr.type == "UNARY":
            right = self.evaluate(expr.right)
            if expr.operator.type == "MINUS":
                return -right
            return None
