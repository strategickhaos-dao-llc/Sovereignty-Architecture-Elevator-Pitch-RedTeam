# src/interpreter.py

class RuntimeReturn(Exception):
    def __init__(self, value):
        self.value = value


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(f"Undefined variable '{name}'.")

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeError(f"Undefined variable '{name}'.")


class KhaosFunction:
    def __init__(self, declaration, closure):
        # declaration: {"type": "FUNCTION" or "LAMBDA", ...}
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        # create new environment with captured closure
        env = Environment(self.closure)
        params = self.declaration["params"]
        for i, param in enumerate(params):
            arg_val = arguments[i] if i < len(arguments) else None
            env.define(param.lexeme, arg_val)

        try:
            interpreter.execute_block(self.declaration["body"], env)
        except RuntimeReturn as r:
            return r.value
        return None


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

    # ===== TOP-LEVEL =====

    def interpret(self, stmts):
        for stmt in stmts:
            if stmt is not None:
                self.execute(stmt)

    # ===== STATEMENTS =====

    def execute(self, stmt):
        stype = stmt["type"]

        if stype == "PRINT":
            value = self.evaluate(stmt["expression"])
            print(value)

        elif stype == "LET":
            value = self.evaluate(stmt["expression"]) if stmt.get("expression") is not None else None
            name = stmt["name"].lexeme
            self.environment.define(name, value)

        elif stype == "EXPR_STMT":
            self.evaluate(stmt["expression"])

        elif stype == "BLOCK":
            self.execute_block(stmt["statements"], Environment(self.environment))

        elif stype == "FUNCTION":
            func = KhaosFunction(stmt, self.environment)
            name = stmt["name"].lexeme
            self.environment.define(name, func)

        elif stype == "RETURN":
            value = None
            if stmt["expression"] is not None:
                value = self.evaluate(stmt["expression"])
            raise RuntimeReturn(value)

        elif stype == "IF":
            cond = self.evaluate(stmt["condition"])
            if self.is_truthy(cond):
                self.execute(stmt["then"])
            elif stmt["else"] is not None:
                self.execute(stmt["else"])

        elif stype == "WHILE":
            while self.is_truthy(self.evaluate(stmt["condition"])):
                self.execute(stmt["body"])

        else:
            raise RuntimeError(f"Unknown statement type {stype}")

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                if stmt is not None:
                    self.execute(stmt)
        finally:
            self.environment = previous

    # ===== EXPRESSIONS =====

    def evaluate(self, expr):
        etype = expr["type"]

        if etype == "LITERAL":
            return expr["value"]

        elif etype == "BINARY":
            left = self.evaluate(expr["left"])
            right = self.evaluate(expr["right"])
            op = expr["operator"].type

            if op == "PLUS":
                # Handle string concatenation with automatic type conversion
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            if op == "MINUS":
                return left - right
            if op == "STAR":
                return left * right
            if op == "SLASH":
                return left / right

            raise RuntimeError(f"Unknown binary operator {op}")

        elif etype == "UNARY":
            right = self.evaluate(expr["right"])
            op = expr["operator"].type
            if op == "MINUS":
                return -right
            raise RuntimeError(f"Unknown unary operator {op}")

        elif etype == "GROUPING":
            return self.evaluate(expr["expression"])

        elif etype == "VARIABLE":
            name = expr["name"].lexeme
            return self.environment.get(name)

        elif etype == "CALL":
            callee = self.evaluate(expr["callee"])
            args = [self.evaluate(a) for a in expr["arguments"]]
            if not isinstance(callee, KhaosFunction):
                raise RuntimeError("Can only call functions for now.")
            return callee.call(self, args)

        elif etype == "LAMBDA":
            # anonymous function; same structure as FUNCTION but no name
            func = KhaosFunction(expr, self.environment)
            return func

        else:
            raise RuntimeError(f"Unknown expression type {etype}")

    # ===== UTILITIES =====

    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return bool(value)
