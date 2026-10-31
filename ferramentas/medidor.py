"""Roda as varreduras e imprime as tabelas do README.

    python -m ferramentas.medidor
    python -m ferramentas.medidor --completo   # crivo ate 10^7

Nenhum numero do README foi digitado a mao, e todos estao presos em
testes/test_medidas.py.
"""

import sys
import time

from totiente.crivo import crivo_de_phi
from totiente.definicao import phi_por_contagem
from totiente.formula import fatorar, phi_por_formula, phi_por_potencias
from totiente.varredura import (
    candidatos_de_lehmer,
    maior_n_com_phi_ate,
    vizinhos_com_o_mesmo_phi,
    conferir_soma_de_gauss,
    menor_razao,
    recordistas_da_razao,
    varrer_imagem,
)

COMPLETO = "--completo" in sys.argv
LIMITE = 10000000 if COMPLETO else 1000000
LIMITE_DA_CONTAGEM = 20000
LIMITE_DE_GAUSS = 200000
TETO_DA_IMAGEM = 100000


def milhar(n):
    return "{:,}".format(n).replace(",", ".")


def main():
    comeco = time.time()

    print("## Os tres caminhos, numero a numero\n")
    phi = crivo_de_phi(LIMITE_DA_CONTAGEM)
    divergencias = 0
    for n in range(1, LIMITE_DA_CONTAGEM + 1):
        if phi_por_formula(n) != phi[n] or phi_por_potencias(n) != phi[n]:
            divergencias += 1
    print("| conferidos pela formula e pelo crivo | divergencias |")
    print("|---|---|")
    print("| %s | %d |" % (milhar(LIMITE_DA_CONTAGEM), divergencias))

    contados = 3000
    divergencias = sum(
        1 for n in range(1, contados + 1) if phi_por_contagem(n) != phi[n]
    )
    print("\n| conferidos tambem pela contagem de coprimos | divergencias |")
    print("|---|---|")
    print("| %s | %d |" % (milhar(contados), divergencias))

    print("\n## A identidade de Gauss: a soma de phi dos divisores da o proprio n\n")
    falhas = conferir_soma_de_gauss(LIMITE_DE_GAUSS)
    print("| conferidos | falhas |")
    print("|---|---|")
    print("| %s | %d |" % (milhar(LIMITE_DE_GAUSS), len(falhas)))

    print("\n## A imagem de phi: quem nunca aparece\n")
    imagem = varrer_imagem(LIMITE)
    nao = imagem.nao_totientes(1000)
    print("varredura de n ate %s, perguntando pelos pares ate 1.000" % milhar(LIMITE))
    print("pares que nao sao valor de phi: %d de 500" % len(nao))
    print("os doze primeiros: %s" % ", ".join(str(v) for v in nao[:12]))
    print("fatia dos pares ate 1.000 que nao sao totientes: %.1f%%" % (100.0 * len(nao) / 500))

    print("\n## A conjectura de Carmichael: nenhum valor aparece uma vez so\n")
    minimo, onde = imagem.multiplicidade_minima(TETO_DA_IMAGEM)
    print("| valores de phi conferidos ate | menor numero de pre-imagens | quantos valores atingem o minimo |")
    print("|---|---|---|")
    print("| %s | %d | %s |" % (milhar(TETO_DA_IMAGEM), minimo, milhar(len(onde))))
    print()
    print("os cinco valores mais populares:")
    for valor, quantos in imagem.mais_populares(5):
        print("  phi(n) = %s acontece com %s numeros" % (milhar(valor), milhar(quantos)))

    print("\n## A varredura foi longe o bastante?\n")
    maior = maior_n_com_phi_ate(LIMITE, TETO_DA_IMAGEM)
    print(
        "maior n ate %s com phi(n) <= %s: %s (%.1f%% do limite)"
        % (milhar(LIMITE), milhar(TETO_DA_IMAGEM), milhar(maior), 100.0 * maior / LIMITE)
    )
    print("entao nenhuma pre-imagem de um valor ate %s ficou de fora." % milhar(TETO_DA_IMAGEM))

    print("\n## O problema de Lehmer: existe composto com phi(n) dividindo n-1?\n")
    achados = candidatos_de_lehmer(LIMITE)
    print("| compostos conferidos ate | achados |")
    print("|---|---|")
    print("| %s | %d |" % (milhar(LIMITE), len(achados)))

    print("\n## Vizinhos com o mesmo phi\n")
    vizinhos = vizinhos_com_o_mesmo_phi(100000)
    print("ate 100.000 sao %s pares; os dez primeiros: %s"
          % (milhar(len(vizinhos)), ", ".join(str(n) for n in vizinhos[:10])))

    print("\n## Quao pequeno phi(n)/n consegue ficar\n")
    print("| n | phi(n) | phi(n)/n | fatorado |")
    print("|---|---|---|---|")
    for n, p, r in recordistas_da_razao(100000):
        fatores = " * ".join(
            "%d^%d" % (q, e) if e > 1 else str(q) for q, e in fatorar(n)
        )
        print("| %s | %s | %.4f | %s |" % (milhar(n), milhar(p), r, fatores))
    n, r = menor_razao(LIMITE)
    print()
    print("ate %s o menor phi(n)/n e %.4f, em n = %s" % (milhar(LIMITE), r, milhar(n)))

    print("\n(medido em %.1f s)" % (time.time() - comeco))


if __name__ == "__main__":
    main()
