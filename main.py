import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import number_input
from consts import MATERIAS, Color


# obtem os anos de participação no enem
while True:
    try:
        anos = [int(i) for i in input("Escreva, separado por espaços, os anos das provas.\n").split()]
        break
    except ValueError:
        print("Tente de novo.")

primeiro_ano = min(anos)
ultimo_ano = max(anos)


def get_notas(ano: int):
    notas = []
    for materia in MATERIAS:
        notas.append(number_input(f"\nInsira a nota de {materia} em {ano}."))

    return notas


# carrega o dicionario com os dados inseridos
dados_dict = {
    "ano_prova": [],
    "materia": [],
    "nota": [],
}
for ano in anos:
    print(f"----- {ano} -----")
    dados_dict["ano_prova"] += [ano] * 5
    dados_dict["materia"] += MATERIAS
    dados_dict["nota"] += get_notas(ano)
    print()

# converte o dicionario para dataframe
dados = pd.DataFrame.from_dict(dados_dict)

fig, ax = plt.subplots()

ax.set_facecolor(Color.GREY98)

# desenha as linhas verticais no grafico
linhas_verticais = np.arange(primeiro_ano, ultimo_ano, 1)
for height in linhas_verticais:
    ax.axvline(height, color=Color.GREY91, lw=1, zorder=0)

# definindo variaveis necessarias para plotar o grafico
lim_y_baixo = dados["nota"].min() - 50 if dados["nota"].min() - 50 >= 0 else 0
lim_y_cima = dados["nota"].max() + 50 if dados["nota"].max() + 50 <= 1000 else 1000

y_start = (lim_y_baixo // 20 - 1) * 20
y_end = (lim_y_cima // 20 + 1) * 20

# desenha as linhas horizontais
ax.hlines(
    y=np.arange(y_start, y_end, 20),
    xmin=primeiro_ano,
    xmax=ultimo_ano + 1,
    color=Color.GREY91,
    lw=1,
)

ax.hlines(
    y=lim_y_baixo,
    xmin=primeiro_ano,
    xmax=ultimo_ano,
    color=Color.GREY60,
    lw=0.8,
)

ax.axvline(ultimo_ano, color=Color.GREY40, ls="dotted")

# coloca uma label no ano mais recente
ax.text(
    ultimo_ano,
    dados["nota"].min(),
    str(ultimo_ano),
    fontsize=14,
    fontweight=500,
    color=Color.GREY40,
    ha="left",
)

# cria as linhas no grafico com os dados do dataset
for materia in MATERIAS:
    row = dados[dados["materia"] == materia]
    color = Color.MATERIAS[materia]
    ax.plot("ano_prova", "nota", color=color, lw=1.8, data=row)

ax.set_xlim(primeiro_ano, ultimo_ano + 1)
ax.set_ylim(lim_y_baixo, lim_y_cima)

# define onde estarao as labels com nome de cada materia
LABEL_Y = list(np.linspace(y_start, y_end, 7))[1:6]

x_start = ultimo_ano
x_end = ultimo_ano + 0.5

# lista de materias ordenadas pelas notas no ultimo ano
materias_ordenadas = dados[(dados["ano_prova"] == ultimo_ano)].sort_values(by="nota")

# cria linhas pontilhadas indicando a label de cada matéria
for index, (_, row) in enumerate(materias_ordenadas.iterrows()):
    color = Color.MATERIAS[row["materia"]]
    text = row["materia"].capitalize()

    y_start = row["nota"]
    y_end = LABEL_Y[index]

    ax.plot(
        [x_start, (x_start + x_end) / 2, x_end],
        [y_start, y_end, y_end],
        color=color,
        alpha=0.5,
        ls="dashed",
    )

    ax.text(x_end, y_end, text, color=color, fontsize=14, weight="bold", va="center")

plt.show()

"""
estrutura do dataset
+-----------+-----------+-------+
|ano_prova  |materia    |nota   |
+-----------+-----------+-------+
|2021       |linguagens |1000.0 |
|2021       |humanas    |1000.0 |
|2021       |natureza   |1000.0 |
|2021       |matematica |1000.0 |
|2021       |redacao    |1000.0 |
|2022       |linguagens |1000.0 |
|2022       |humanas    |1000.0 |
|2022       |natureza   |1000.0 |
|2022       |matematica |1000.0 |
|2022       |redacao    |1000.0 |
+-----------+-----------+-------+
"""
