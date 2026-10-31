"""Os numeros do README, presos.

Todos saem de `python -m ferramentas.medidor`. Se a medida mudar, a bateria
quebra antes do texto.
"""

import unittest

from totiente.formula import fatorar
from totiente.varredura import (
    candidatos_de_lehmer,
    conferir_soma_de_gauss,
    maior_n_com_phi_ate,
    menor_razao,
    recordistas_da_razao,
    varrer_imagem,
    vizinhos_com_o_mesmo_phi,
)

IMAGEM = varrer_imagem(1000000)


class TestGauss(unittest.TestCase):
    def test_duzentos_mil_sem_falha(self):
        self.assertEqual(conferir_soma_de_gauss(200000), [])


class TestNaoTotientes(unittest.TestCase):
    def test_quantos_pares_ate_mil_nunca_aparecem(self):
        nao = IMAGEM.nao_totientes(1000)
        self.assertEqual(len(nao), 210)
        self.assertAlmostEqual(100.0 * len(nao) / 500, 42.0, places=1)

    def test_os_doze_primeiros(self):
        self.assertEqual(
            IMAGEM.nao_totientes(1000)[:12],
            [14, 26, 34, 38, 50, 62, 68, 74, 76, 86, 90, 94],
        )

    def test_a_varredura_foi_longe_o_bastante(self):
        maior = maior_n_com_phi_ate(1000000, 100000)
        self.assertEqual(maior, 510510)
        self.assertAlmostEqual(100.0 * maior / 1000000, 51.1, places=1)


class TestCarmichael(unittest.TestCase):
    def test_o_minimo_de_preimagens_e_dois(self):
        minimo, onde = IMAGEM.multiplicidade_minima(100000)
        self.assertEqual(minimo, 2)
        self.assertEqual(len(onde), 7785)

    def test_os_cinco_valores_mais_populares(self):
        self.assertEqual(
            IMAGEM.mais_populares(5),
            [
                (241920, 937),
                (207360, 750),
                (181440, 734),
                (161280, 718),
                (201600, 716),
            ],
        )

    def test_o_campeao_e_muito_divisivel(self):
        self.assertEqual(fatorar(241920), [(2, 8), (3, 3), (5, 1), (7, 1)])


class TestLehmer(unittest.TestCase):
    def test_nenhum_composto_ate_um_milhao(self):
        self.assertEqual(candidatos_de_lehmer(1000000), [])


class TestRazao(unittest.TestCase):
    def test_os_seis_recordistas_ate_cem_mil(self):
        esperado = [
            (2, 1, 0.5000),
            (6, 2, 0.3333),
            (30, 8, 0.2667),
            (210, 48, 0.2286),
            (2310, 480, 0.2078),
            (30030, 5760, 0.1918),
        ]
        medido = recordistas_da_razao(100000)
        self.assertEqual(len(medido), len(esperado))
        for (n, p, r), (en, ep, er) in zip(medido, esperado):
            self.assertEqual(n, en)
            self.assertEqual(p, ep)
            self.assertAlmostEqual(r, er, places=4)

    def test_o_menor_ate_um_milhao(self):
        n, r = menor_razao(1000000)
        self.assertEqual(n, 510510)
        self.assertAlmostEqual(r, 0.1805, places=4)
        self.assertEqual(fatorar(510510), [(2, 1), (3, 1), (5, 1), (7, 1), (11, 1), (13, 1), (17, 1)])


class TestVizinhos(unittest.TestCase):
    def test_trinta_e_seis_pares_ate_cem_mil(self):
        self.assertEqual(len(vizinhos_com_o_mesmo_phi(100000)), 36)

    def test_os_dez_primeiros(self):
        self.assertEqual(
            vizinhos_com_o_mesmo_phi(100000)[:10],
            [1, 3, 15, 104, 164, 194, 255, 495, 584, 975],
        )
