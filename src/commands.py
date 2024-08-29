from src.exceptions import *


class Command:
    def __init__(self, function):
        # Function of the arithmetic module to be executed
        self.function = function
        self.last_args = None

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        return [int(args)]

    def parse_output(self, output) -> str:
        """
        Parses the output to a string.
        """
        return str(output)

    def execute(self, args: str) -> str:
        # Parse and check the arguments
        try:
            parsed_args = self.parse_check_args(args)
        except:
            raise InvalidArgs(f"InvalidArgsError: {args}")
        self.last_args = parsed_args
        # Execute the function
        output = self.function(*parsed_args)
        # Parse the output
        return self.parse_output(output)


class EsPrimo(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        return [int(args)]

    def parse_output(self, output) -> str:
        return "Sí" if output else "No"


class ListaPrimos(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        if len(args) != 2:
            raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
        return [int(args[0]), int(args[1])]

    def parse_output(self, output) -> str:
        if len(output) == 0:
            a, b = self.last_args
            raise NoSolution(f"NoSolutionError: No primes in range [{a},{b})")
        return ", ".join([str(x) for x in output])


class Factorizar(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        return [abs(int(args))]

    def parse_output(self, output) -> str:
        return ", ".join([f"{x}: {output[x]}" for x in output])


class MCD(Command):
    def __init__(self, function, function_n):
        super().__init__(function)
        self.function_n = function_n

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        return [abs(int(arg)) for arg in args.split(",")]

    def execute(self, args: str) -> str:
        # Parse and check the arguments
        try:
            parsed_args = self.parse_check_args(args)
        except:
            raise InvalidArgs(f"InvalidArgsError: {args}")
        self.last_args = parsed_args
        # Execute the function
        if len(parsed_args) == 2:
            output = self.function(*parsed_args)
        else:
            output = self.function_n(parsed_args)
        # Parse the output
        return self.parse_output(output)


class Bezout(Command):
    def __init__(self, function, function_n):
        super().__init__(function)
        self.function_n = function_n

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        return [int(arg) for arg in args]

    def parse_output(self, output) -> str:
        return f"{output[0]}, {output[1]}, {output[2]}"

    def execute(self, args: str) -> str:
        # Parse and check the arguments
        try:
            parsed_args = self.parse_check_args(args)
        except:
            raise InvalidArgs(f"InvalidArgsError: {args}")
        self.last_args = parsed_args
        # Execute the function
        if len(parsed_args) == 2:
            output = self.function(*parsed_args)
        else:
            output = self.function_n(parsed_args)
        # Parse the output
        return self.parse_output(output)


class Coprimos(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        if len(args) != 2:
            raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
        return [int(args[0]), int(args[1])]

    def parse_output(self, output) -> str:
        return "Sí" if output else "No"


class PotenciaModP(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        if len(args) != 3:
            raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
        return [int(args[0]), int(args[1]), int(args[2])]


class InversoModP(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        if len(args) != 2:
            raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
        return [int(args[0]), int(args[1])]


class Euler(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        return [int(args)]


class Legendre(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        if len(args) != 2:
            raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
        return [int(args[0]), int(args[1])]


class ResolverSistema(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        args_t = [[], [], []]
        for i in range(len(args)):
            args[i] = args[i][1:-1].split(";")
            if len(args[i]) != 3:
                raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
            args_t[0].append(int(args[i][0]))
            args_t[1].append(int(args[i][1]))
            args_t[2].append(int(args[i][2]))
        return args_t

    def parse_output(self, output) -> str:
        return f"{output[0]} (mod {output[1]})"


class RaizModP(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        if len(args) != 2:
            raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
        return [int(args[0]), int(args[1])]

    def parse_output(self, output) -> str:
        r = output
        r2 = self.last_args[1] - r
        if r < r2:
            return f"{r}, {r2}"
        elif r2 < r:
            return f"{r2}, {r}"
        else:
            return f"{r}"


class EcuacionCuadratica(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        if len(args) != 4:
            raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
        return [int(args[0]), int(args[1]), int(args[2]), int(args[3])]

    def parse_output(self, output) -> str:
        x1, x2 = output
        if x1 == x2:
            return f"{x1}"
        if x1 > x2:
            return f"{x2}, {x1}"
        return f"{x1}, {x2}"


class MCM(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        return [abs(int(arg)) for arg in args]


class StrongPseudoPrime(Command):
    def __init__(self, function):
        super().__init__(function)

    def parse_check_args(self, args: str) -> list:
        """
        Parses and checks the arguments.
        """
        args = args.split(",")
        if len(args) != 2:
            raise InvalidArgs(f"InvalidArgsError: Wrong number of arguments")
        return [int(args[0]), int(args[1])]

    def parse_output(self, output) -> str:
        return "Sí" if output else "No"
