import sys
from src.commands import *
from src.exceptions import *
import src.modular as modular
import re


imatlab_interface = None


class Imatlab:
    def __init__(self):
        self.COMMANDS = {
            "primo": EsPrimo(modular.es_primo),
            "primos": ListaPrimos(modular.lista_primos),
            "factorizar": Factorizar(modular.factorizar),
            "mcd": MCD(modular.mcd, modular.mcd_n),
            "bezout": Bezout(modular.bezout, modular.bezout_n),
            "coprimos": Coprimos(modular.coprimos),
            "pow": PotenciaModP(modular.potencia_mod_p),
            "inv": InversoModP(modular.inverso_mod_p),
            "euler": Euler(modular.euler),
            "legendre": Legendre(modular.legendre),
            "resolverSistema": ResolverSistema(modular.resolver_sistema_congruencias),
            "raiz": RaizModP(modular.raiz_mod_p),
            "ecCuadratica": EcuacionCuadratica(modular.ecuacion_cuadratica),
            "mcm": MCM(modular.mcm),
            "spp": StrongPseudoPrime(modular.spp),
        }
        self.command_pattern = re.compile(
            r"^([plwcmbdzrnaoiegvfutCsS]+)\(([0-9,;\-\[\]]+)\)\s*$"
        )

    def parse_command(self, raw_input: str) -> tuple[str, list]:
        """
        Recieves raw input from user and returns a tuple with the name of the command
        and a list with the arguments.
        """
        name, args = self.command_pattern.match(raw_input).groups()
        return name, args

    def execute_command(self, raw_input: str) -> str:
        """
        Recieves raw input command, converts it to a name and args and executes it.
        Returns output as a string.
        Controls possible errors.
        """
        try:
            name, args = self.parse_command(raw_input)
        except:
            raise InvalidInput(f"InvalidInputError: '{raw_input.strip()}'")

        if name not in self.COMMANDS:
            raise InvalidCommand(f"InvalidCommandError: '{name}'")

        output = self.COMMANDS[name].execute(args)

        return output

    def start_interface(self):
        try:
            print("Welcome to Imatlab!")
            print("Enter ctrl+c to exit")
            print("The commands are in the form: name(args)")
            raw_input = input(">>> ")
        except KeyboardInterrupt:
            return
        while raw_input.strip() not in ["exit", "quit", ""]:
            try:
                print(self.execute_command(raw_input))
            except Exception as e:
                print(e)
            try:
                raw_input = input(">>> ")
            except KeyboardInterrupt:
                return

    def run_batch(self, fin: str, fout: str):
        try:
            file_in = open(fin, "r")
        except:
            print(f"FileError: Cannot open in file '{fin}'")
            return
        try:
            file_out = open(fout, "w", encoding="utf-8")
        except:
            print(f"FileError: Cannot open out file '{fout}'")
            return
        output = ""
        for line in file_in:
            try:
                output += self.execute_command(line) + "\n"
            except Exception as e:
                if hasattr(e, "type") and e.type == "NE":
                    output += "NE" + "\n"
                elif hasattr(e, "type") and e.type == "NOP":
                    output += "NOP" + "\n"
                else:
                    output += "NOP" + "\n"
        try:
            file_out.write(output)
        except:
            print(f"FileError: Could not write to file '{fout}'")


if not imatlab_interface:
    imatlab_interface = Imatlab()


def run_commands(fin, fout):
    """
    Ejecuta los comandos del archivo de entrada y los en el archivo de salida.
    fin: TextIO
    fout: TextIO
    """
    output = ""
    for line in fin:
        try:
            output += imatlab_interface.execute_command(line) + "\n"
        except Exception as e:
            if hasattr(e, "type") and e.type == "NE":
                output += "NE" + "\n"
            elif hasattr(e, "type") and e.type == "NOP":
                output += "NOP" + "\n"
            else:
                output += "NOP" + "\n"
    try:
        fout.write(output)
    except:
        print(f"FileError: Could not write to file '{fout}'")


if __name__ == "__main__":

    if not imatlab_interface:
        imatlab_interface = Imatlab()

    if len(sys.argv) == 1:
        imatlab_interface.start_interface()
    elif len(sys.argv) == 2:
        print("SysArgsError: Missing one argument (Posibly the output file)")
    elif len(sys.argv) == 3:
        imatlab_interface.run_batch(sys.argv[1], sys.argv[2])
    else:
        print("SysArgsError: Too many arguments")
