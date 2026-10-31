"""A definicao, sem atalho nenhum: contar quem nao tem fator em comum com n.

Este e o caminho mais lento dos tres e e por isso que ele existe. Quando a
formula e o crivo concordam entre si, pode ser que os dois estejam errados do
mesmo jeito; a contagem nao compartilha uma linha com nenhum deles.
"""

from math import gcd


def phi_por_contagem(n):
    """Quantos numeros de 1 a n sao coprimos com n."""
    if n < 1:
        raise ValueError("%d nao e positivo" % n)
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def coprimos(n):
    """A lista de quem e coprimo com n, de 1 a n."""
    return [k for k in range(1, n + 1) if gcd(k, n) == 1]


def divisores(n):
    """Todos os divisores de n, em ordem crescente."""
    pequenos = []
    grandes = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            pequenos.append(d)
            if d != n // d:
                grandes.append(n // d)
        d += 1
    return pequenos + grandes[::-1]
