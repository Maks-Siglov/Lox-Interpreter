class ParserError(RuntimeError):
    pass


class Return(RuntimeError):
    def __init__(self, value):
        super().__init__()
        self.value = value


class ResolveError(RuntimeError):
    pass
