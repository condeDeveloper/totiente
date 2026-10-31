"""O segundo caminho: fatorar e aplicar o produto de Euler.

phi(n) = n * produto de (1 - 1/p) sobre os primos p que dividem n.

A conta e feita em inteiros, como `n // p * (p - 1)`, e nunca em ponto
flutuante: `n * (1 - 1/3)` em double devolve 6.000000000000001 para n = 9.
"""


def fatorar(n):
    """A fatoracao de n como lista de (primo, expoente), por divisao de teste."""
    if n < 1:
        raise ValueError("%d nao e positivo" % n)
    fatores = []
    m = n
    expoente = 0
    while m % 2 == 0:
        m //= 2
        expoente += 1
    if expoente:
        fatores.append((2, expoente))
    d = 3
    while d * d <= m:
        expoente = 0
        while m % d == 0:
            m //= d
            expoente += 1
        if expoente:
            fatores.append((d, expoente))
        d += 2
    if m > 1:
        fatores.append((m, 1))
    return fatores


def phi_por_formula(n):
    """phi(n) pelo produto de Euler, em aritmetica inteira."""
    if n < 1:
        raise ValueError("%d nao e positivo" % n)
    resultado = n
    for p, _ in fatorar(n):
        resultado = resultado // p * (p - 1)
    return resultado


def phi_por_potencias(n):
    """phi(n) multiplicando phi de cada potencia de primo.

    phi e multiplicativa: phi(p^k) = p^(k-1) * (p-1), e phi(a*b) = phi(a)*phi(b)
    quando a e b sao coprimos. Este caminho usa a multiplicatividade; o outro
    usa o produto. Eles podem discordar se a fatoracao estiver errada, e e por
    isso que os dois estao aqui.
    """
    resultado = 1
    for p, k in fatorar(n):
        resultado *= p ** (k - 1) * (p - 1)
    return resultado
