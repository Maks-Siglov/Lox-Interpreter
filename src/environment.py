class Environment:
    def __init__(self, enclosing=None):
        self.var_values = {}
        self.enclosing = enclosing

    def define_var(self, name, value) -> None:
        self.var_values[name] = value

    def get_var(self, name):
        if name in self.var_values:
            return self.var_values[name]
        elif self.enclosing is not None:
            return self.enclosing.get_var(name)
        raise RuntimeError(f"Undefined variable {name}.")

    def assign(self, name, value):
        if name in self.var_values:
            self.var_values[name] = value
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError(name, f"Undefined variable '{name}'.")
