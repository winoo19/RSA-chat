import src.modular as modular
import random
from src.exceptions import NoSolution


def generar_claves(min_primo: int, max_primo: int) -> tuple:
    """
    Z x Z -> (Z, Z) x (Z, Z)
    Devuelve primos en el intervalo [min_primo, max_primo)
    ~10^100 -> 5 segundos
    """
    min_primo = max(min_primo, 2)
    r = max_primo - min_primo
    if r <= 2:
        raise NoSolution("No hay suficientes primos")
    else:
        p, q = None, None
        inicio_p = random.randint(0, r - 1)
        i = inicio_p
        while not modular.es_primo(min_primo + i):
            i = (i + 1) % r
            if i == inicio_p:
                raise NoSolution("No hay suficientes primos")
        p = min_primo + i
        fin_p = i
        l = r - (fin_p - inicio_p) if fin_p >= inicio_p else inicio_p - fin_p
        inicio_q = (fin_p + random.randint(1, l - 1)) % r
        i = inicio_q
        while i != inicio_p and not modular.es_primo(min_primo + i):
            i = (i + 1) % r
        if i == inicio_p:
            i = inicio_q - 1
            while i != fin_p and not modular.es_primo(min_primo + i):
                i = (i - 1) % r
            if i == fin_p:
                raise NoSolution("No hay suficientes primos")
        q = min_primo + i
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while modular.mcd(e, phi) != 1:
        e = (e + 2) % phi
    d = modular.inverso_mod_p(e, phi)
    return (n, e), (n, d)


def aplicar_padding(m: int, digitos_padding: int) -> int:
    """
    Z x Z -> Z
    Rellena m con cifras aleatorias
    """
    pad = "".join([str(random.randint(0, 9)) for _ in range(digitos_padding)])
    return int(str(m) + pad)


def eliminar_padding(m: int, digitos_padding: int) -> int:
    """
    Z x Z -> Z
    """
    return int(str(m)[:-digitos_padding])


def cifrar_rsa(m: int, n: int, e: int, digitos_padding: int) -> int:
    """
    Z x Z x Z x Z -> Z
    """
    cifrado = modular.potencia_mod_p(aplicar_padding(m, digitos_padding), e, n)
    return cifrado


def descifrar_rsa(c: int, n: int, d: int, digitos_padding: int) -> int:
    """
    Z x Z x Z x Z -> Z
    """
    return eliminar_padding(modular.potencia_mod_p(c, d, n), digitos_padding)


def cifrar_cadena_rsa(s: str, n: int, e: int, digitos_padding: int) -> list[int]:
    """
    String x Z x Z x Z -> Z
    """
    c = []
    for ch in s:
        c.append(cifrar_rsa(ord(ch), n, e, digitos_padding))
    return c


def descifrar_cadena_rsa(cList: list[int], n: int, d: int, digitos_padding: int) -> str:
    """
    Z x Z x Z x Z -> String
    """
    s = []
    for c in cList:
        s.append(chr(descifrar_rsa(c, n, d, digitos_padding)))
    return "".join(s)


def romper_clave(n: int, e: int) -> int:
    """
    Z x Z -> Z
    """
    seed = 4
    g = lambda x: (x**2 - 5) % n
    p = n
    while p == n:
        p = modular.imatlab_module.pollard_rho_brent_module(n, seed, g)
        seed += 1
    if p == 1:
        raise NoSolution("N debe ser compuesto")
    q = n // p
    phi = (p - 1) * (q - 1)
    d = modular.inverso_mod_p(e, phi)
    return d


def ataque_texto_plano(cList: list[int], n: int, e: int) -> str:
    """
    Z x Z x Z -> String
    """
    dic = {}
    for c in range(2**16):
        dic[cifrar_rsa(c, n, e, 0)] = c
    return "".join([chr(dic[c]) for c in cList])


def ataque_ciclico(cList: list[int], n: int, e: int) -> str:
    """
    Z x Z x Z -> String
    If we find l such that c^(e^l) = 1 mod n, then we can find m = c^(e^(l-1)) mod n
    We know l|lambda(lambda(n)), with lambda(n) = lcm(p-1, q-1)
    Only works with small e and l
    """
    l = 2
    cypher = cList[0]
    while modular.potencia_mod_p(cypher, pow(e, l), n) != cypher:
        l += 1
    m = modular.potencia_mod_p(cypher, pow(e, l - 2), n)
    return m
