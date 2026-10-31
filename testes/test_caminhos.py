"""Os tres caminhos de phi, conferidos um contra o outro."""

import unittest
from math import gcd

from totiente.crivo import crivo_de_phi
from totiente.definicao import coprimos, divisores, phi_por_contagem
from totiente.formula import fatorar, phi_por_formula, phi_por_potencias

PHI = crivo_de_phi(20000)


class TestDefinicao(unittest.TestCase):
    def test_os_primeiros_valores(self):
        primeiros = [phi_por_contagem(n) for n in range(1, 21)]
        self.assertEqual(
            primeiros,
            [1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4, 12, 6, 8, 8, 16, 6, 18, 8],
        )

    def test_phi_de_primo_e_p_menos_um(self):
        for p in (2, 3, 5, 7, 11, 13, 101, 997):
            self.assertEqual(phi_por_contagem(p), p - 1, "p=%d" % p)

    def test_coprimos_sao_mesmo_coprimos(self):
        for n in range(1, 200):
            lista = coprimos(n)
            self.assertEqual(len(lista), phi_por_contagem(n))
            for k in lista:
                self.assertEqual(gcd(k, n), 1)

    def test_recusa_zero_e_negativo(self):
        for n in (0, -1, -100):
            with self.assertRaises(ValueError):
                phi_por_contagem(n)

    def test_divisores(self):
        self.assertEqual(divisores(1), [1])
        self.assertEqual(divisores(12), [1, 2, 3, 4, 6, 12])
        self.assertEqual(divisores(36), [1, 2, 3, 4, 6, 9, 12, 18, 36])


class TestFatoracao(unittest.TestCase):
    def test_casos(self):
        self.assertEqual(fatorar(1), [])
        self.assertEqual(fatorar(2), [(2, 1)])
        self.assertEqual(fatorar(360), [(2, 3), (3, 2), (5, 1)])
        self.assertEqual(fatorar(1000003), [(1000003, 1)])

    def test_o_produto_devolve_o_numero(self):
        for n in range(1, 3000):
            produto = 1
            for p, k in fatorar(n):
                produto *= p ** k
            self.assertEqual(produto, n, "n=%d" % n)


class TestOsTresConcordam(unittest.TestCase):
    def test_formula_contra_crivo(self):
        for n in range(1, 20001):
            self.assertEqual(phi_por_formula(n), PHI[n], "n=%d" % n)

    def test_potencias_contra_crivo(self):
        for n in range(1, 20001):
            self.assertEqual(phi_por_potencias(n), PHI[n], "n=%d" % n)

    def test_contagem_contra_os_outros(self):
        for n in range(1, 3001):
            esperado = phi_por_contagem(n)
            self.assertEqual(esperado, PHI[n], "n=%d" % n)
            self.assertEqual(esperado, phi_por_formula(n), "n=%d" % n)

    def test_multiplicativa_em_coprimos(self):
        for a in range(1, 60):
            for b in range(1, 60):
                if gcd(a, b) == 1:
                    self.assertEqual(
                        PHI[a * b], PHI[a] * PHI[b], "a=%d b=%d" % (a, b)
                    )

    def test_nao_e_multiplicativa_fora_dos_coprimos(self):
        # 2 e 4 nao sao coprimos: phi(8) = 4, mas phi(2) * phi(4) = 2
        self.assertEqual(PHI[8], 4)
        self.assertNotEqual(PHI[8], PHI[2] * PHI[4])

    def test_phi_e_par_depois_do_dois(self):
        for n in range(3, 20001):
            self.assertEqual(PHI[n] % 2, 0, "n=%d" % n)
