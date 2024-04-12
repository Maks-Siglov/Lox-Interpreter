class Environment:
    def __init__(self):
        self.var_values = {}

    def define_var(self, name, value) -> None:
        self.var_values[name] = value

    def get_var(self, name):
        if name in self.var_values:
            return self.var_values[name]
        raise RuntimeError(f"Undefined variable {name.lexeme}.")
