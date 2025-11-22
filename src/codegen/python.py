class PythonCodegen:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    def emit(self, line=""):
        self.code.append("    " * self.indent_level + line)

    def generate(self, stmts):
        self.emit("# StrategicKhaos → Python transpiled on 2025-11-21")
        self.emit("variables = {}")
        self.emit()

        for stmt in stmts:
            self.visit_stmt(stmt)

        self.emit()
        return "\n".join(self.code)

    def visit_stmt(self, stmt):
        if stmt.type == "PRINT":
            value = self.visit_expr(stmt.expression)
            self.emit(f"print({value})")
        elif stmt.type == "LET":
            value = self.visit_expr(stmt.expression)
            name = stmt.name.lexeme
            self.emit(f"variables['{name}'] = {value}")

    def visit_expr(self, expr):
        if expr.type == "LITERAL":
            if isinstance(expr.value, str):
                return f'"{expr.value}"'
            return str(expr.value)
        elif expr.type == "BINARY":
            left = self.visit_expr(expr.left)
            right = self.visit_expr(expr.right)
            op = {
                "PLUS": "+",
                "MINUS": "-",
                "STAR": "*",
                "SLASH": "/",
            }[expr.operator.type]
            return f"({left} {op} {right})"
        elif expr.type == "GROUPING":
            return f"({self.visit_expr(expr.expression)})"
        elif expr.type == "VARIABLE":
            return f"variables['{expr.name.lexeme}']"
        elif expr.type == "UNARY":
            right = self.visit_expr(expr.right)
            if expr.operator.type == "MINUS":
                return f"(-{right})"
            return right
        raise Exception(f"Unknown expr: {expr}")
