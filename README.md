# A função totiente de Euler

`phi(n)` é quantos números de 1 a `n` não têm fator em comum com `n`. Euler a
publicou em 1763, e ela aparece em todo lugar: é o expoente que faz o teorema de
Euler funcionar, é o tamanho do grupo multiplicativo módulo `n`, e é o que torna
o RSA possível.

Aqui ela é calculada por **três caminhos que não compartilham uma linha de
código** — a contagem de coprimos, que é a definição; o produto de Euler sobre
os primos que dividem `n`; e um crivo que resolve todo o intervalo de uma vez
sem fatorar ninguém. Depois disso, o repositório faz as perguntas que a fórmula
não responde. Python puro, sem dependência nenhuma.

## Os quatro achados

1. **42% dos pares até 1.000 nunca são valor de `phi`.** São 210 dos 500, e o
   primeiro é o **14**. A varredura vai a 1.000.000 e a resposta é honesta: o
   maior `n` até um milhão com `phi(n) <= 100.000` é **510.510**, só 51,1% do
   limite, então nenhuma pré-imagem ficou de fora.
2. **Nenhum valor de `phi` aparece uma vez só, em 100.000 valores conferidos.**
   É a conjectura de Carmichael, aberta desde 1907: o mínimo de pré-imagens é
   **2**, e 7.785 valores atingem esse mínimo. No outro extremo, `phi(n) =
   241.920` acontece com **937 números diferentes**.
3. **Nenhum composto até um milhão tem `phi(n)` dividindo `n-1`.** É o problema
   de Lehmer, de 1932: para primo sempre funciona, porque `phi(p) = p-1`;
   para composto ninguém achou um exemplo nem provou que não existe.
4. **Quem minimiza `phi(n)/n` é sempre primorial, mas quem maximiza `n` com
   `phi` limitado não é.** O menor `phi(n)/n` até um milhão é **0,1805**, em
   510.510 = 2·3·5·7·11·13·17. Já o maior `n` com `phi(n) <= 10.000` é
   **46.410 = 2·3·5·7·13·17**, e não o primorial 30.030: trocar o 11 por 13 e 17
   custa pouco em `phi` e rende muito em `n`.

## As tabelas

Tudo abaixo sai de `python -m ferramentas.medidor`. Nenhum número foi digitado à
mão, e todos estão presos em `testes/test_medidas.py`.

### Os três caminhos, número a número

| conferidos | pelo quê | divergências |
|---|---|---|
| 20.000 | fórmula, multiplicatividade e crivo | 0 |
| 3.000 | os três acima mais a contagem de coprimos | 0 |

A contagem de coprimos é `O(n log n)` por número e por isso só vai a 3.000. Ela
é a única que não depende de fatorar nada, e é a razão de existir das outras
duas.

### A identidade de Gauss

| conferidos | falhas |
|---|---|
| 200.000 | 0 |

A soma de `phi(d)` sobre os divisores de `n` dá o próprio `n`. Gauss provou em
1801; aqui a soma é calculada sem usar o fato, espalhando cada `phi(d)` nos
múltiplos de `d`.

### A imagem de phi

| o que | quanto |
|---|---|
| varredura de `n` até | 1.000.000 |
| pares até 1.000 que não são valor de `phi` | 210 de 500 (42,0%) |
| os doze primeiros | 14, 26, 34, 38, 50, 62, 68, 74, 76, 86, 90, 94 |
| maior `n` com `phi(n) <= 100.000` | 510.510 (51,1% do limite) |

Nenhum ímpar além do 1 é valor de `phi`, e isso também está em teste: `phi(n)` é
par para todo `n` maior que 2.

### A conjectura de Carmichael

| valores conferidos até | menor número de pré-imagens | quantos valores atingem o mínimo |
|---|---|---|
| 100.000 | 2 | 7.785 |

Os cinco valores mais populares:

| phi(n) | quantos n | fatorado |
|---|---|---|
| 241.920 | 937 | 2⁸ · 3³ · 5 · 7 |
| 207.360 | 750 | |
| 181.440 | 734 | |
| 161.280 | 718 | |
| 201.600 | 716 | |

### Quão pequeno `phi(n)/n` consegue ficar

| n | phi(n) | phi(n)/n | fatorado |
|---|---|---|---|
| 2 | 1 | 0,5000 | 2 |
| 6 | 2 | 0,3333 | 2 · 3 |
| 30 | 8 | 0,2667 | 2 · 3 · 5 |
| 210 | 48 | 0,2286 | 2 · 3 · 5 · 7 |
| 2.310 | 480 | 0,2078 | 2 · 3 · 5 · 7 · 11 |
| 30.030 | 5.760 | 0,1918 | 2 · 3 · 5 · 7 · 11 · 13 |

Seis recordes em cem mil números, e todos primoriais. Até um milhão entra o
sétimo: 510.510, com 0,1805.

### O problema de Lehmer e os vizinhos

| o que | quanto |
|---|---|
| compostos conferidos até | 1.000.000 |
| compostos com `phi(n)` dividindo `n-1` | 0 |
| pares `phi(n) = phi(n+1)` até 100.000 | 36 |
| os dez primeiros | 1, 3, 15, 104, 164, 194, 255, 495, 584, 975 |

## O que as medidas me corrigiram

Os erros são meus, não do Euler.

- **Supus que o maior `n` com `phi(n)` limitado fosse um primorial.** Escrevi o
  teste com 30.030 e ele quebrou: é **46.410**. O primorial minimiza a razão
  `phi(n)/n`, que é outra pergunta. Para esticar o `n` com `phi` preso, vale
  trocar um primo por dois primos um pouco maiores.
- **Chutei o expoente dentro do arquivo que existe para impedir chute.** Escrevi
  que 241.920 é `2⁷ · 3³ · 5 · 7`. É `2⁸`. O `test_medidas.py` pegou na mesma
  rodada em que foi escrito.
- **Esperava que a conjectura de Carmichael fosse apertada.** Não é: além de
  nenhum valor ter uma pré-imagem só, **7.785 valores têm exatamente duas**, o
  que mostra que o mínimo é atingido o tempo todo e não é um caso de borda.
- **Achei que a contagem de coprimos serviria para o domínio inteiro.** Ela é
  quadrática no total e empaca bem antes: acima de poucos milhares, o crivo
  resolve em um segundo o que ela levaria minutos para fazer. Por isso cada
  tabela diz até onde cada caminho foi.

## Como está organizado

```
totiente/definicao.py   a definição: contar coprimos com mdc, sem atalho
totiente/formula.py     o produto de Euler e a multiplicatividade, em inteiros
totiente/crivo.py       o crivo que resolve o intervalo inteiro sem fatorar
totiente/varredura.py   imagem, Carmichael, Lehmer, razão mínima e vizinhos
ferramentas/medidor.py  roda tudo e imprime as tabelas acima
testes/                 39 testes
```

Por que a fórmula é calculada como `n // p * (p - 1)` e não como
`n * (1 - 1/p)`: em ponto flutuante a segunda forma devolve `6.000000000000001`
para `n = 9`, e `phi` é inteiro por definição.

## Rodar

```bash
python -m unittest discover -s testes -t . -v   # a bateria inteira
python -m ferramentas.medidor                   # recalcula as tabelas deste README
python -m ferramentas.medidor --completo        # crivo até 10 milhões
```

Sem `pip install`: não há dependência. Precisa de Python 3.11 ou mais novo.

## Licença

MIT.
