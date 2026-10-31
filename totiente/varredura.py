"""O que se pergunta DEPOIS de saber calcular phi.

Tres perguntas, todas respondidas por varredura e nenhuma por formula:

* quais pares nunca aparecem como valor de phi (os nao-totientes);
* quantos numeros compartilham cada valor de phi (a conjectura de Carmichael);
* quao pequeno phi(n)/n consegue ficar.
"""

from .crivo import crivo_de_phi


class Imagem:
    """Quem aparece como valor de phi ate um limite, e quantas vezes."""

    def __init__(self, limite, quantos, phi):
        self.limite = limite
        self.quantos = quantos  # {valor: quantidade de n <= limite com phi(n) = valor}
        self.phi = phi

    def nao_totientes(self, ate):
        """Os pares de 2 ate `ate` que nao sao valor de phi de ninguem.

        So vale perguntar ate um teto bem menor que o limite da varredura: se
        phi(n) = v entao n < v * 7 para todo v testado aqui, mas a garantia
        honesta e varrer n ate um multiplo folgado do teto e dizer qual foi.
        """
        return [v for v in range(2, ate + 1, 2) if v not in self.quantos]

    def multiplicidade_minima(self, ate):
        """O menor numero de pre-imagens entre os valores de phi ate `ate`."""
        valores = {v: q for v, q in self.quantos.items() if 0 < v <= ate}
        minimo = min(valores.values())
        return minimo, sorted(v for v, q in valores.items() if q == minimo)

    def mais_populares(self, quantos=5):
        return sorted(self.quantos.items(), key=lambda par: (-par[1], par[0]))[:quantos]


def varrer_imagem(limite):
    """Calcula phi de 1 a `limite` e agrupa pelos valores."""
    phi = crivo_de_phi(limite)
    quantos = {}
    for n in range(1, limite + 1):
        quantos[phi[n]] = quantos.get(phi[n], 0) + 1
    return Imagem(limite, quantos, phi)


def menor_razao(limite):
    """O n <= limite com o menor phi(n)/n, e a razao dele.

    O recordista e sempre um primorial: para baixar a razao vale mais um primo
    novo e pequeno do que repetir um que ja esta la.
    """
    phi = crivo_de_phi(limite)
    melhor = 2
    razao = phi[2] / 2
    for n in range(2, limite + 1):
        r = phi[n] / n
        if r < razao:
            melhor, razao = n, r
    return melhor, razao


def recordistas_da_razao(limite):
    """Todo n que baixa o recorde de phi(n)/n, em ordem."""
    phi = crivo_de_phi(limite)
    saida = []
    melhor = None
    for n in range(2, limite + 1):
        r = phi[n] / n
        if melhor is None or r < melhor:
            melhor = r
            saida.append((n, phi[n], r))
    return saida


def candidatos_de_lehmer(limite):
    """Os compostos n com phi(n) dividindo n - 1.

    Lehmer perguntou em 1932 se existe algum. Noventa e quatro anos depois
    ninguem achou nem provou que nao existe. Para os primos a divisao sempre
    funciona, porque phi(p) = p - 1, entao eles nao contam.
    """
    phi = crivo_de_phi(limite)
    saida = []
    for n in range(3, limite + 1, 2):
        if (n - 1) % phi[n] == 0 and phi[n] != n - 1:
            saida.append(n)
    return saida


def vizinhos_com_o_mesmo_phi(limite):
    """Os n com phi(n) = phi(n+1)."""
    phi = crivo_de_phi(limite + 1)
    return [n for n in range(1, limite + 1) if phi[n] == phi[n + 1]]


def maior_n_com_phi_ate(limite, teto):
    """O maior n <= limite cujo phi nao passa de `teto`.

    Serve para saber se a varredura foi longe o bastante: se este numero fica
    bem abaixo de `limite`, nenhuma pre-imagem de um valor <= teto ficou de
    fora, e a tabela dos nao-totientes vale de verdade.
    """
    phi = crivo_de_phi(limite)
    for n in range(limite, 0, -1):
        if phi[n] <= teto:
            return n
    return 0


def conferir_soma_de_gauss(limite):
    """Quantos n de 1 a `limite` falham a identidade de Gauss. Deve dar zero."""
    from .crivo import soma_dos_phi_dos_divisores

    soma = soma_dos_phi_dos_divisores(limite)
    return [n for n in range(1, limite + 1) if soma[n] != n]
