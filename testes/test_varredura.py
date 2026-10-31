"""As perguntas que vem depois de saber calcular phi."""

import unittest

from totiente.crivo import crivo_de_phi, soma_dos_phi_dos_divisores
from totiente.definicao import divisores
from totiente.formula import phi_por_formula
from totiente.varredura import (
    candidatos_de_lehmer,
    conferir_soma_de_gauss,
    maior_n_com_phi_ate,
    menor_razao,
    recordistas_da_razao,
    varrer_imagem,
    vizinhos_com_o_mesmo_phi,
)


class TestIdentidadeDeGauss(unittest.TestCase):
    def test_sem_falha_ate_cinquenta_mil(self):
        self.assertEqual(conferir_soma_de_gauss(50000), [])

    def test_o_crivo_de_somas_bate_com_a_definicao(self):
        soma = soma_dos_phi_dos_divisores(2000)
        for n in range(1, 2001):
            manual = sum(phi_por_formula(d) for d in divisores(n))
            self.assertEqual(soma[n], manual, "n=%d" % n)


class TestImagem(unittest.TestCase):
    def test_os_primeiros_nao_totientes(self):
        imagem = varrer_imagem(100000)
        self.assertEqual(
            imagem.nao_totientes(100),
            [14, 26, 34, 38, 50, 62, 68, 74, 76, 86, 90, 94, 98],
        )

    def test_nenhum_impar_fora_do_um_e_totiente(self):
        imagem = varrer_imagem(100000)
        impares = [v for v in imagem.quantos if v % 2 and v != 1]
        self.assertEqual(impares, [])

    def test_a_varredura_cobre_os_valores_que_ela_afirma(self):
        # se o maior n com phi(n) <= teto fica longe do limite, nada ficou fora.
        # e NAO e o primorial 30.030: 46.410 = 2*3*5*7*13*17 tem phi = 9.216,
        # porque trocar o 11 por 13 e 17 custa pouco em phi e rende muito em n
        self.assertEqual(maior_n_com_phi_ate(100000, 10000), 46410)
        self.assertEqual(maior_n_com_phi_ate(100000, 1000), 4620)
        self.assertLess(maior_n_com_phi_ate(100000, 10000), 100000)

    def test_carmichael_nao_falha_no_dominio_varrido(self):
        imagem = varrer_imagem(100000)
        minimo, _ = imagem.multiplicidade_minima(10000)
        self.assertEqual(minimo, 2)

    def test_quem_atinge_o_minimo_tem_mesmo_duas_preimagens(self):
        imagem = varrer_imagem(100000)
        _, onde = imagem.multiplicidade_minima(10000)
        for valor in onde[:50]:
            quantos = sum(1 for n in range(1, 100001) if imagem.phi[n] == valor)
            self.assertEqual(quantos, 2, "valor=%d" % valor)


class TestLehmer(unittest.TestCase):
    def test_nenhum_composto_ate_duzentos_mil(self):
        self.assertEqual(candidatos_de_lehmer(200000), [])

    def test_os_primos_sempre_funcionariam(self):
        phi = crivo_de_phi(1000)
        primos = [p for p in range(2, 1001) if phi[p] == p - 1]
        for p in primos:
            self.assertEqual((p - 1) % phi[p], 0)


class TestRazao(unittest.TestCase):
    def test_os_recordistas_sao_primoriais(self):
        esperado = [2, 6, 30, 210, 2310, 30030]
        self.assertEqual([n for n, _, _ in recordistas_da_razao(100000)], esperado)

    def test_a_razao_cai_sempre(self):
        anterior = 1.0
        for _, _, r in recordistas_da_razao(100000):
            self.assertLess(r, anterior)
            anterior = r

    def test_o_menor_de_todos_ate_cem_mil(self):
        n, r = menor_razao(100000)
        self.assertEqual(n, 30030)
        self.assertAlmostEqual(r, 0.1918, places=4)


class TestVizinhos(unittest.TestCase):
    def test_os_primeiros(self):
        self.assertEqual(
            vizinhos_com_o_mesmo_phi(1000),
            [1, 3, 15, 104, 164, 194, 255, 495, 584, 975],
        )

    def test_cada_par_bate_mesmo(self):
        phi = crivo_de_phi(1001)
        for n in vizinhos_com_o_mesmo_phi(1000):
            self.assertEqual(phi[n], phi[n + 1], "n=%d" % n)
