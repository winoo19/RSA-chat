class InvalidInput(Exception):
    def __init__(self, message):
        self.message = message
        self.type = "NOP"
        super().__init__(message)


class InvalidCommand(Exception):
    def __init__(self, message):
        self.message = message
        self.type = "NOP"
        super().__init__(message)


class InvalidArgs(Exception):
    def __init__(self, message):
        self.message = message
        self.type = "NOP"
        super().__init__(message)


class NoSolution(Exception):
    def __init__(self, message):
        self.message = message
        self.type = "NE"
        super().__init__(message)


class InfiniteSolutions(Exception):
    def __init__(self, message):
        self.message = message
        self.type = "NE"
        super().__init__(message)
