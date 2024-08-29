import math
import numpy as np
from src.exceptions import *

imatlab_module = None


"""
Modulo de Aritmetica Modular
"""


class Module:
    def __init__(self):
        self.cache = {}
        self.fp2 = Fp2(self.legendre_module)

    def a_sprp_module(self, n: int, a: int, d: int, s: int) -> bool:
        """
        Z x Z x Z x Z-> Bool
        Comprueba si n es un pseudo primo fuerte para base a
        """
        x = self.potencia_mod_p_module(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    def es_primo_module(self, n: int) -> bool:
        """
        Z -> Bool
        Comprueba si n es un primo con el test determinista de miller
        """
        if n <= 1 or n % 2 == 0:
            return False if n != 2 else True
        exceptions = {
            25326001,
            161304001,
            960946321,
            1157839381,
            3215031751,
            3697278427,
            5764643587,
            6770862367,
        }
        if n in exceptions:
            return False
        if n <= 2047:
            bases = [2]
        elif n <= 1373653:
            bases = [2, 3]
        elif n < 14386156093:
            bases = [2, 3, 5]
        else:
            bases = self.lista_primos_module(2, int(2 * math.log(n) ** 2) + 1)
        d, s = n - 1, 0
        while d & 1 == 0:
            d = d >> 1
            s += 1
        for a in bases:
            if not self.a_sprp_module(n, a, d, s):
                return False
        return True

    def lista_primos_simple_module(self, a: int, b: int) -> list:
        """
        Z x Z -> [Z]
        Devuelve una lista de los numeros primos en [a, b) usando el algoritmo de criba de eratostenes simple
        """
        primos = []
        es_primo = [True] * b
        for i in range(2, b):
            if es_primo[i]:
                if i >= a:
                    primos.append(i)
                for j in range(i * i, b, i):
                    es_primo[j] = False
        return primos

    def lista_primos_module(self, a: int, b: int) -> list:
        """
        Z x Z -> [Z]
        Devuelve una lista de los numeros primos en [a, b)
        """
        a = max(a, 2)
        if a * a > b:
            root = int(math.sqrt(b))
            primos = []
            es_primo = [True] * (root + 1)
            for i in range(2, (root + 1)):
                if es_primo[i]:
                    primos.append(i)
                    for j in range(i * i, root, i):
                        es_primo[j] = False
            es_primo_ab = [True] * (b - a)
            for primo in primos:
                for i in range(((-a) % primo), b - a, primo):
                    es_primo_ab[i] = False
            primos_ab = []
            for i in range(b - a):
                if es_primo_ab[i]:
                    primos_ab.append(i + a)
            return primos_ab
        else:
            return self.lista_primos_simple_module(a, b)

    def factorizar_simple_module(self, n: int):
        """
        Z -> [Z]
        Devuelve los factores primos de n mayores que 41 dentro de un diccionario en O(sqrt(n))
        """
        factors = {}
        i, root = 41, int(math.sqrt(n))
        while i <= root:
            reduced = False
            while n % i == 0:
                n //= i
                factors[i] = factors.get(i, 0) + 1
                reduced = True
            i += 2
            if i <= root:
                while n % i == 0:
                    n //= i
                    factors[i] = factors.get(i, 0) + 1
                    reduced = True
            if n == 1:
                return factors
            if reduced:
                root = int(math.sqrt(n))
            i += 4
        if n > 1:
            factors[n] = 1
        return factors

    def pollard_rho_floyd_module(self, n: int, seed: int, g=None) -> int:
        """
        Z x Z -> Z
        Devuelve un factor de n usando el algoritmo rho de pollard optimizado con
        el algoritmo de floyd y la variante de paquetes
        """

        if not g:
            g = lambda x: (x**2 + 1) % n

        x = y = seed
        d = packet = c = 1
        while d == 1:
            x = g(x)
            y = g(g(y))
            packet = ((x - y) * packet) % n
            if c == 64:
                d = self.mcd_simple_module(packet, n)
                c = 0
                packet = 1
            c += 1
        return d

    def pollard_rho_brent_module(self, n: int, seed: int, g: callable = None) -> int:
        """
        Z x Z -> Z
        Devuelve un factor de n usando el algoritmo rho de pollard optimizado con
        el algoritmo de brent y la variante de paquetes
        """

        if not g:
            g = lambda x: (x**2 + 1) % n

        x = seed
        y = g(seed)
        d = packet = c = power = pos = 1
        while d == 1:
            if power == pos:
                x = y
                power *= 2
                pos = 0
            y = g(y)
            pos += 1
            previous_packet = packet
            packet = ((x - y) * packet) % n
            if packet == 0:
                return self.mcd_simple_module(previous_packet, n)
            if c == 100:
                d = self.mcd_simple_module(packet, n)
                c = 0
                packet = 1
            c += 1
        return d

    def factorizar_module(self, n: int) -> dict[int, int]:
        """
        Z -> {Z: Z, ...}
        Devuelve un diccionario con los factores primos de n y sus exponentes
        """
        if n == 0:
            raise InfiniteSolutions(
                "InfiniteSolutionsError: 0 has infinite prime factors"
            )
        elif n == 1:
            raise NoSolution("NoSolutionError: 1 has no prime factors")
        factors = dict()
        firsts = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        for primo in firsts:
            while n % primo == 0:
                n //= primo
                factors[primo] = factors.get(primo, 0) + 1
            if n == 1:
                return factors
        if n < 10**10:
            return {**factors, **self.factorizar_simple_module(n)}
        else:
            seed = 2
            while seed < 6:
                d = self.pollard_rho_brent_module(n, seed)
                if d != n:
                    return {
                        **factors,
                        **self.factorizar_module(d),
                        **self.factorizar_module(n // d),
                    }
                seed += 1
            return {**factors, **self.factorizar_simple_module(n)}

    def mcd_simple_module(self, a: int, b: int) -> int:
        """
        Z x Z -> Z
        Devuelve el maximo comun divisor de a y b usando euclides
        """
        if a > b:
            a, b = b, a
        while b:
            a, b = b, a % b
        return a

    def mcd_module(self, a: int, b: int) -> int:
        """
        Z^n -> Z
        Devuelve el maximo comun divisor de a y b usando least absolute remainder.
        """
        if a > b:
            a, b = b, a
        while a:
            r, b = b % a, a
            if r > a >> 1:
                a = a - r
            else:
                a = r
        return b

    def bezout_module(self, a: int, b: int) -> tuple[int, int, int]:
        """
        Z^n -> (Z, Z, Z)
        Devuelve una tupla (d,x,y) donde d es el mcd(a,b) y (x,y) es una solucion particular de d = ax + by
        """
        swap = False
        if a > b:
            a, b = b, a
            swap = True

        a_coeffs = np.array([1, 0], dtype=object)
        b_coeffs = np.array([0, 1], dtype=object)

        while a:
            a_coeffs, b_coeffs = b_coeffs - a_coeffs * (b // a), a_coeffs
            a, b = b % a, a
        if swap:
            b_coeffs = b_coeffs[::-1]
        return b, int(b_coeffs[0]), int(b_coeffs[1])

    def mcd_n_module(self, nlist: list) -> int:
        """
        [Z] -> Z
        Devuelve el maximo comun divisor de los numeros de nlist
        """
        gcd = nlist[0]
        for i in range(1, len(nlist)):
            gcd = self.mcd_module(gcd, nlist[i])
            if gcd == 1:
                return 1
        return gcd

    def bezout_n_module(self, nlist: list) -> tuple[int, list]:
        """
        [Z] -> (Z, [Z])
        Devuelve una tupla (d,x) donde d es el mcd de los coeficientes y x es una solucion particular
        de d = c1*x1 + c2*x2 + ... + cn*xn
        """
        length = len(nlist)
        coeffs = [
            np.array([0] * i + [1] + [0] * (length - i - 1), dtype=np.int64)
            for i in range(length)
        ]
        i = 0
        count_zeros = 0
        while count_zeros != length - 1:
            m = nlist[i]
            if m == 0:
                i = (i + 1) % length
                continue
            count_zeros = 0
            for j in range(length):
                if i == j:
                    continue
                num = nlist[j]
                if num == 0:
                    count_zeros += 1
                    continue
                nlist[j] = num % m
                coeffs[j] -= coeffs[i] * (num // m)
            i = (i + 1) % length
        return m, list(coeffs[(i - 1) % length])

    def coprimos_module(self, a: int, b: int) -> bool:
        """
        Z x Z -> Bool
        Comprueba si dos numeros son coprimos.
        Mas rapido con mcd_simple por el tamaño de los numeros.
        """
        if (a | b) & 1 == 0:
            return False
        return self.mcd_simple_module(a, b) == 1

    def potencia_mod_p_module(self, base: int, exp: int, p: int) -> int:
        """
        Z x Z x Z -> Z
        Devuelve base^exp mod p
        Raises an exception if exp < 0 and base is not invertible mod p
        """
        if exp < 0:
            base = self.inverso_mod_p_module(base, abs(p))
            exp = -exp
        potencia = 1
        bin_str = bin(exp)
        base = base % p
        for i in range(len(bin_str) - 1, 1, -1):
            if bin_str[i] == "1":
                potencia = (potencia * base) % p
            base = (base * base) % p
        return potencia

    def inverso_mod_p_module(self, n: int, p: int) -> int:
        """
        Z x Z -> Z
        Devuelve el inverso de n mod p
        Raises an exception if n is not invertible mod p or n is 0 or p is 1 or 0
        """
        p = abs(p)
        n = n % p
        if n == 0 or p == 1 or p == 0:
            raise NoSolution(f"NoSolutionError: {n} no tiene inversa mod {p}")
        a, m = n, p
        a_coeff, b_coeff = 1, 0
        while a:
            a_coeff, b_coeff = b_coeff - a_coeff * (m // a), a_coeff
            m, a = a, m % a
        if m != 1:
            raise NoSolution(f"NoSolutionError: {n} no tiene inversa mod {p}")
        return b_coeff % p

    def euler_module(self, n: int) -> int:
        """
        Z -> Z
        Devuelve el valor de euler totient of n
        """
        tot = abs(n)
        firsts = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        for primo in firsts:
            if n % primo == 0:
                tot -= tot // primo
                while n % primo == 0:
                    n = n // primo
                if n == 1:
                    return tot
        i, root = 41, int(math.sqrt(n))
        while i <= root:
            f1, f2 = i, i + 2
            reduced = False
            if n % f1 == 0:
                tot -= tot // f1
                reduced = True
                while n % f1 == 0:
                    n //= f1
            if n % f2 == 0:
                tot -= tot // f2
                reduced = True
                while n % f2 == 0:
                    n //= f2
            if n == 1:
                return tot
            if reduced:
                root = int(math.sqrt(n))
            i += 6
        if n > 1:
            tot -= tot // n
        return tot

    def legendre_module(self, n: int, p: int) -> int:
        """
        Z x Z -> Z
        Devuelve el simbolo de legendre de n y p
        """
        if p == 2:
            return 1
        l = self.potencia_mod_p_module(n, (p - 1) // 2, p)
        if l not in (0, 1):
            return -1
        return l

    def resolver_sistema_congruencias_module(
        self, alist: list, blist: list, plist: list
    ) -> tuple:
        """
        [Z] x [Z] x [Z] -> (Z, [Z])
        Resuelve el sistema de congruencias lineal y devuelve una tupla (r,m) donde r es la solucion modulo m.
        Raises an exception if the system has no solution or has infinite solutions
        """
        size = len(plist)
        for k in range(size - 1, -1, -1):
            a, b, p = alist[k], blist[k], plist[k]
            if p != 1:
                gcd = self.mcd_simple_module(self.mcd_simple_module(a, b), p)
                a, b, p = a // gcd, b // gcd, p // gcd
                blist[k], plist[k] = (b % p) * self.inverso_mod_p_module(a, p) % p, p
                alist[k] = 1
            else:
                alist.pop(k)
                blist.pop(k)
                plist.pop(k)
        size = len(plist)
        if size == 0:
            raise InfiniteSolutions("InfiniteSolutionsError: all x of Z are solutions")
        for i in range(size - 2, -1, -1):
            a1, m1 = blist[i + 1], plist[i + 1]
            a2, m2 = blist[i], plist[i]
            g, p, q = self.bezout_module(m1, m2)
            if a1 == a2:
                plist[i] = (m1 * m2) // g
            else:
                if (a1 - a2) % g != 0:
                    raise NoSolution(f"NoSolutionError: No solution exists")
                plist[i] = (m1 * m2) // g
                blist[i] = (a1 * (m2 // g) * q + a2 * (m1 // g) * p) % plist[i]
        return blist[0] % plist[0], plist[0]

    def raiz_mod_p_module(self, n: int, p: int) -> int:
        """
        Z x Z -> Z
        Devuelve una raiz cuadrada de n mod p
        Raises an exception if n is not a quadratic residue mod p
        """
        n %= p
        if self.legendre_module(n, p) == -1:
            raise NoSolution(f"{n} no tiene raiz cuadrada mod {p}")
        if p % 4 == 3:
            return self.potencia_mod_p_module(n, (p + 1) // 4, p)
        elif p % 8 == 5:
            posible_sol = self.potencia_mod_p_module(n, (p + 3) // 8, p)
            if posible_sol**2 % p == n:
                return posible_sol
            return (posible_sol * self.potencia_mod_p_module(2, (p - 1) // 4, p)) % p
        else:
            return self.fp2.sqrt(n % p, p)

    def ecuacion_cuadratica_module(
        self, a: int, b: int, c: int, p: int
    ) -> tuple[int, int]:
        """
        Z x Z x Z x Z -> (Z, Z)
        Devuelve una solucion de la ecuacion ax^2 + bx + c = 0 mod p
        """
        a, b, c = a % p, b % p, c % p
        sqrt = self.raiz_mod_p_module((b * b - 4 * a * c) % p, p)
        x1 = (-b + sqrt) * self.inverso_mod_p_module(2 * a, p)
        x2 = (-b - sqrt) * self.inverso_mod_p_module(2 * a, p)
        return x1 % p, x2 % p

    def mcm_module(self, *args) -> int:
        """
        Z x Z -> Z
        Devuelve el minimo comun multiplo de los numeros dados
        """
        mcm = 1
        for n in args:
            mcm *= n // self.mcd_simple_module(mcm, n)
        return mcm

    def primitive_root_module(self, p: int) -> int:
        """
        Z -> Z
        Devuelve una raiz primitiva (generador) de Zp*
        Only works for n of the form 1, 2, 4, p^k or 2*p^k for p odd prime
        """
        if p == 1:
            return 0
        elif p == 2:
            return 1
        elif p == 4:
            return 3
        phi = self.euler_module(p)
        factorization = self.factorizar_module(phi)
        factors = list(factorization.keys())
        for r in range(2, p):
            if self.mcd_module(r, p) == 1:
                valido, i = True, 0
                while valido and i < len(factors):
                    if self.potencia_mod_p_module(r, phi // factors[i], p) in (0, 1):
                        valido = False
                    i += 1
                if valido:
                    # for exp in range(1, phi + 1):
                    #     print(f"{r}^{exp} = {self.potencia_mod_p_module(r, exp, p)}")
                    return r
        raise NoSolution(f"NoSolutionError: No primitive root found for {p}")

    def carmichael_pt_module(self, p: int, e: int) -> int:
        """
        Z x Z -> Z
        Devuelve el carmichael de p^e
        """
        if p == 2 and e >= 3:
            return pow(2, e - 2)
        return pow(p, e - 1) * (p - 1)

    def carmichael_module(self, n: int) -> int:
        """
        Z -> Z
        Devuelve el numero de Carmichael de n
        """
        factorization = self.factorizar_module(n)
        return self.mcm_module(
            *[self.carmichael_pt_module(p, factorization[p]) for p in factorization]
        )


"""
Fp^2 field
"""


class Fp2:
    def __init__(self, legendre):
        self.legendre = legendre

    def find_generator(self, n: int, p: int) -> int:
        """
        Finds a such that a^2 - n is not a quadratic residue mod p
        """
        a = 2
        while self.legendre(a * a - n, p) != -1:
            a += 1
        self.a = a
        self.w2 = a * a - n

    def mult(self, x: tuple, y: tuple, p: int) -> tuple:
        """
        Multiplication in Fp2
        """
        real = x[0] * y[0] + x[1] * y[1] * self.w2
        imag = x[0] * y[1] + x[1] * y[0]
        return real % p, imag % p

    def exp(self, x: tuple, exp: int, p: int) -> tuple:
        """
        Binary exponentiation in Fp2
        """
        potencia = (1, 0)
        bin_str = bin(exp)
        base = x
        for i in range(len(bin_str) - 1, 1, -1):
            if bin_str[i] == "1":
                potencia = self.mult(potencia, base, p)
            base = self.mult(base, base, p)
        return potencia

    def sqrt(self, n: int, p: int) -> int:
        """
        Finds a square root of n as the 'real' part of (a+sqrt(a*a-n))**((p+1)//2) element of Fp2
        """
        self.find_generator(n, p)
        return self.exp((self.a, 1), (p + 1) // 2, p)[0]


"""Create module"""

if not imatlab_module:
    imatlab_module = Module()


def es_primo(n: int) -> bool:
    """
    Z -> Bool
    Comprueba si un numero es primo
    """
    return imatlab_module.es_primo_module(n)


def lista_primos(a: int, b: int) -> list:
    """
    Z -> List
    Devuelve una lista con los primos entre a y b
    """
    return imatlab_module.lista_primos_module(a, b)


def factorizar(n: int) -> dict[int, int]:
    """
    Z -> {Z: Z}
    Devuelve el factorizacion de n
    """
    return imatlab_module.factorizar_module(n)


def mcd(a: int, b: int) -> int:
    """
    Z x Z -> Z
    Devuelve el maximo comun divisor de a y b
    """
    return imatlab_module.mcd_module(a, b)


def bezout(a: int, b: int) -> tuple[int, int, int]:
    """
    Z x Z -> (Z, Z, Z)
    Devuelve una tupla (d,x,y) donde d es el mcd de a y b y x,y son soluciones particulares de d = ax + by
    """
    return imatlab_module.bezout_module(a, b)


def mcd_n(nlist: list) -> int:
    """
    [Z] -> Z
    Devuelve el maximo comun divisor de los elementos de la lista
    """
    return imatlab_module.mcd_n_module(nlist)


def bezout_n(nlist: list) -> tuple:
    """
    [Z] -> (Z, [Z])
    Devuelve una tupla (d, x) donde d es el mcd de los elementos de la lista y x es una lista de soluciones particulares de
    d = x1 * n1 + x2 * n2 + ... + xn * nn
    """
    return imatlab_module.bezout_n_module(nlist)


def coprimos(a: int, b: int) -> bool:
    """
    Z x Z -> Bool
    Comprueba si dos numeros son coprimos
    """
    return imatlab_module.coprimos_module(a, b)


def potencia_mod_p(base: int, exp: int, p: int) -> int:
    """
    Z x Z x Z -> Z
    Devuelve base^exp mod p
    Raise an exception if exp < 0 and base is not invertible mod p
    """
    return imatlab_module.potencia_mod_p_module(base, exp, p)


def inverso_mod_p(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve el inverso de n mod p
    Raise an exception if n is not invertible mod p
    """
    return imatlab_module.inverso_mod_p_module(n, p)


def euler(n: int) -> int:
    """
    Z -> Z
    Devuelve el valor de euler totient of n
    """
    return imatlab_module.euler_module(n)


def legendre(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve el simbolo de legendre de n y p
    """
    return imatlab_module.legendre_module(n, p)


def resolver_sistema_congruencias(alist: list, blist: list, plist: list) -> tuple:
    """
    [Z] x [Z] x [Z] -> (Z, [Z])
    Resuelve el sistema de congruencias lineal y devuelve una tupla (r,m) donde r es la solucion modulo m
    """
    return imatlab_module.resolver_sistema_congruencias_module(alist, blist, plist)


def raiz_mod_p(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve una raiz cuadrada de n mod p
    """
    return imatlab_module.raiz_mod_p_module(n, p)


def ecuacion_cuadratica(a: int, b: int, c: int, p: int) -> tuple[int, int]:
    """
    Z x Z x Z x Z -> (Z, Z)
    Devuelve las raices de la ecuacion ax^2 + bx + c = 0 mod p
    """
    return imatlab_module.ecuacion_cuadratica_module(a, b, c, p)


def mcm(*args) -> int:
    """
    Z x Z -> Z
    Devuelve el minimo comun multiplo de a y b
    """
    return imatlab_module.mcm_module(*args)


def spp(n: int, a: int) -> bool:
    """
    Z x Z -> Bool
    Comprueba si n es un numero de strong pseudoprime base a
    n must be an odd composite number
    """
    if n % 2 == 0 or es_primo(n) or n <= 1:
        return False
    a %= n
    d, s = n - 1, 0
    while d & 1 == 0:
        d = d >> 1
        s += 1
    return imatlab_module.a_sprp_module(n, a, d, s)


def primitive_root(p: int) -> int:
    """
    Z -> Z
    Devuelve una raiz primitiva de p
    """
    return imatlab_module.primitive_root_module(p)
