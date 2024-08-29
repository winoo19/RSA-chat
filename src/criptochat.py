import src.rsa as rsa
import os
import sys
import signal
import json


def signal_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

chat = None


class CriptoChat:
    def __init__(self):
        self.users = self.load_users()
        self.current_user = None
        self.digitos_padding = 5
        self.UNICODE = 1114111

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    def save_users(self):
        try:
            with open("users.json", "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=4)
        except Exception as e:
            print("Error al guardar los usuarios:", e.__class__.__name__, e)

    def registrar_usuario(self):
        os.system("cls|clear")
        print(" " * 15 + "Registro de usuario")
        nombre = input("\nNombre de usuario: ")
        while nombre in self.users and self.current_user is None:
            os.system("cls|clear")
            print("El nombre de usuario ya existe")
            print("\n1. Volver a intentarlo")
            print("2. Log in")
            print("3. Salir")
            option = input("\n-> ")
            while option not in ["1", "2", "3"]:
                print("Opción inválida")
                option = input("\n-> ")
            if option == "1":
                os.system("cls|clear")
                nombre = input("Nombre de usuario: ")
            elif option == "2":
                self.login()
                return
            elif option == "3":
                sys.exit()
        contraseña = input("Contraseña: ")
        while len(contraseña) < 4:
            print("La contraseña debe tener al menos 4 caracteres")
            contraseña = input("Contraseña: ")
        self.users[nombre] = {
            "nombre": nombre,
            "contraseña": contraseña,
        }
        error = True
        while error:
            try:
                rango = map(int, input("Rango de la clave ('a b'): ").split())
                pk, sk = rsa.generar_claves(*rango)
                error = False
            except Exception as e:
                print("Rango inválido", e.__class__.__name__, e)
        self.users[nombre]["pk"] = pk
        self.users[nombre]["sk"] = sk
        self.users[nombre]["contactos"] = {}
        self.current_user = self.users[nombre]
        self.save_users()
        print("\nUsuario registrado!")
        print("Clave pública:", pk)
        print("Clave privada:", sk)

    def login(self):
        os.system("cls|clear")
        print(" " * 15 + "Log in")
        nombre = input("\nNombre de usuario: ")
        contraseña = input("Contraseña: ")
        if nombre in self.users and self.users[nombre]["contraseña"] == contraseña:
            self.current_user = self.users[nombre]
        else:
            os.system("cls|clear")
            if nombre not in self.users:
                print("El usuario no existe")
            else:
                print("Contraseña incorrecta")
            print("\n1. Registrarse")
            print("2. Volver a intentarlo")
            print("3. Salir")
            option = input("\n-> ")
            while option not in ["1", "2", "3"]:
                print("Opción inválida")
                option = input("\n-> ")
            if option == "1":
                self.registrar_usuario()
            elif option == "2":
                self.login()
            elif option == "3":
                sys.exit()

    def start_menu(self):
        """Log in or register"""
        while self.current_user is None:
            os.system("cls|clear")
            print(" " * 15 + "CriptoChat: Inicio")
            print("\n1. Register")
            print("2. Log in")
            print("3. Exit")
            option = input("\n-> ")
            while option not in ["1", "2", "3"]:
                print("Opción inválida")
                option = input("\n-> ")
            if option == "1":
                self.registrar_usuario()
            elif option == "2":
                self.login()
            elif option == "3":
                sys.exit()

    def generar_claves(self):
        os.system("cls|clear")
        print(" " * 15 + "Generar claves")
        error = True
        while error:
            try:
                rango = map(int, input("\nRango de la clave ('a b'): ").split())
                pk, sk = rsa.generar_claves(*rango)
                error = False
            except Exception as e:
                print("Rango inválido", e.__class__.__name__, e)
        self.current_user["pk"] = pk
        self.current_user["sk"] = sk
        self.save_users()
        print("\nNueva clave pública:", pk)
        print("Nueva clave privada:", sk)

    def registrar_claves(self):
        os.system("cls|clear")
        print(" " * 15 + "Registrar claves")
        error = True
        while error:
            try:
                n = int(input("\nn: "))
                e = int(input("e: "))
                d = int(input("d: "))
                error = False
            except Exception as e:
                print("Error:", e)
        self.current_user["pk"] = (n, e)
        self.current_user["sk"] = (n, d)
        self.save_users()
        print("\nNueva clave pública:", (n, e))
        print("Nueva clave privada:", (n, d))

    def añadir_contacto(self):
        os.system("cls|clear")
        print(" " * 15 + "Añadir contacto")
        print("\nContactos:", ", ".join(self.current_user["contactos"].keys()), "\n")
        nombre = input("\nNombre del contacto: ")
        while len(nombre) == 0:
            print("Nombre inválido")
            nombre = input("Nombre del contacto: ")
        print("Clave pública del contacto:")
        error = True
        while error:
            try:
                n = int(input("n: "))
                e = int(input("e: "))
                error = False
            except Exception as e:
                print("Error:", e)
        self.current_user["contactos"][nombre] = {"nombre": nombre, "pk": (n, e)}
        self.save_users()
        print("\nContacto registrado!")

    def enviar_mensaje(self):
        os.system("cls|clear")
        print(" " * 15 + "Enviar mensaje")
        print("\nContactos:", ", ".join(self.current_user["contactos"].keys()), "\n")
        nombre = input("\nNombre del contacto: ")
        while nombre not in self.current_user["contactos"]:
            os.system("cls|clear")
            print("Contacto no encontrado!")
            print("\n1. Añadir contacto")
            print("2. Volver a intentarlo")
            print("3. Salir")
            option = input("\n-> ")
            while option not in ["1", "2", "3"]:
                print("Opción inválida")
                option = input("\n-> ")
            if option == "1":
                self.añadir_contacto()
                return
            elif option == "2":
                self.enviar_mensaje()
                return
            elif option == "3":
                sys.exit(0)
        m = input("Mensaje: ")
        while len(m) == 0:
            print("Mensaje inválido")
            m = input("Mensaje: ")
        n, e = self.current_user["contactos"][nombre]["pk"]
        c = rsa.cifrar_cadena_rsa(m, n, e, self.digitos_padding)
        print("\nMensaje cifrado:", " ".join(map(str, c)))

    def recibir_mensaje(self):
        os.system("cls|clear")
        print(" " * 15 + "Recibir mensaje")
        error = True
        while error:
            c = input("\nMensaje cifrado: ")
            try:
                c = list(map(int, c.split()))
                n, d = self.current_user["sk"]
                m = rsa.descifrar_cadena_rsa(c, n, d, self.digitos_padding)
                print("\nMensaje:", m)
                error = False
            except TypeError:
                print("Mensaje inválido")
            except:
                print("Error: Tus claves no son válidas o el mensaje es erroneo.")
                error = False

    def cambiar_padding(self):
        os.system("cls|clear")
        print(" " * 15 + "Cambiar padding")
        error = True
        while error:
            try:
                self.digitos_padding = int(input("\nDigitos de padding: "))
                error = False
            except Exception as e:
                print("Error:", e)
        print("\nPadding cambiado!")

    def cambiar_usuario(self):
        self.current_user = None
        self.start_menu()

    def modificar_contacto(self):
        os.system("cls|clear")
        if len(self.current_user["contactos"]) == 0:
            print("\nNo tienes contactos!")
            return
        print(" " * 15 + "Modificar contacto")
        print("\nContactos:", ", ".join(self.current_user["contactos"].keys()), "\n")
        nombre = input("\nNombre del contacto antiguo: ")
        while nombre not in self.current_user["contactos"]:
            os.system("cls|clear")
            print("Contacto no encontrado!")
            nombre = input("\nNombre del contacto antiguo: ")
        print("1. Cambiar nombre")
        print("2. Cambiar clave pública")
        print("3. Eliminar contacto")
        option = input("\n-> ")
        while option not in ["1", "2", "3"]:
            print("Opción inválida")
            option = input("\n-> ")
        if option == "1":
            nombre_nuevo = input("Nombre del contacto nuevo: ")
            while len(nombre_nuevo) == 0 or self.current_user["contactos"]:
                print(
                    "Nombre inválido"
                    if len(nombre_nuevo) == 0
                    else "El contacto ya existe!"
                )
                nombre_nuevo = input("Nombre del contacto nuevo: ")

            self.current_user["contactos"][nombre_nuevo] = {"nombre": nombre_nuevo}
        elif option == "2":
            print("Clave pública del contacto:")
            error = True
            while error:
                try:
                    n = int(input("n: "))
                    e = int(input("e: "))
                    error = False
                except Exception as e:
                    print("Error:", e)
            self.current_user["contactos"][nombre_nuevo]["pk"] = (n, e)
        elif option == "3":
            del self.current_user["contactos"][nombre]
        self.save_users()
        print("\nContacto modificado!")

    def chat_menu(self):
        salir = False
        while not salir:
            os.system("cls|clear")
            print(
                " " * 15 + "CriptoChat" + " " * 5 + "👤 " + self.current_user["nombre"]
            )
            print("\n1. Generar un nuevo par de claves")
            print("2. Registrar un nuevo par de claves")
            print("3. Añadir contacto")
            print("4. Enviar mensaje")
            print("5. Recibir mensaje")
            print("6. Cambiar padding")
            print("7. Cambiar de usuario")
            print("8. Modificar contacto")
            print("9. Salir")
            option = input("\n-> ")
            while option not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                print("Opción inválida")
                option = input("\n-> ")
            if option == "1":
                self.generar_claves()
            elif option == "2":
                self.registrar_claves()
            elif option == "3":
                self.añadir_contacto()
            elif option == "4":
                self.enviar_mensaje()
            elif option == "5":
                self.recibir_mensaje()
            elif option == "6":
                self.cambiar_padding()
            elif option == "7":
                self.cambiar_usuario()
            elif option == "8":
                self.modificar_contacto()
            elif option == "9":
                sys.exit(0)
            input("\nPresione enter para continuar...")

    def interfaz(self):
        self.start_menu()
        input("\nPresione enter para continuar...")
        self.chat_menu()


if chat is None:
    chat = CriptoChat()

if __name__ == "__main__":
    chat.interfaz()
