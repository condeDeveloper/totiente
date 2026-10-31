"""O terceiro caminho: um crivo que calcula phi de TODOS de uma vez.

Nao fatora ninguem. Comeca com phi[n] = n e, para cada primo encontrado,
desconta a fatia 1/p de todos os multiplos dele. No fim phi[n] esta pronto para
todo n do intervalo, e o custo e o mesmo do crivo de Eratostenes.
"""


def crivo_de_phi(limite):
    """Lista com phi(0..limite). phi(0) nao existe e fica 0."""
    phi = list(range(limite + 1))
    for p in range(2, limite + 1):
        if phi[p] == p:  # p ainda intacto, logo e primo
            for multiplo in range(p, limite + 1, p):
                phi[multiplo] -= phi[multiplo] // p
    phi[0] = 0
    return phi


def soma_dos_phi_dos_divisores(limite):
    """Para cada n, a soma de phi(d) sobre os divisores d de n.

    Gauss provou em 1801 que essa soma e sempre o proprio n. Aqui ela e
    calculada sem usar esse fato: cada d espalha o seu phi(d) nos multiplos.
    """
    phi = crivo_de_phi(limite)
    soma = [0] * (limite + 1)
    for d in range(1, limite + 1):
        for multiplo in range(d, limite + 1, d):
            soma[multiplo] += phi[d]
    return soma
