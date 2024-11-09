import matplotlib.pyplot as plt

with open("E:\\#ESTUDOS\\datafinanceflask\\data\\statusinvest-busca-avancada.csv", encoding="utf-8") as file:
    dados = file.readlines()

nomes = []
valores = []

for i in range(len(dados)):
    if i != 0:
        linha = dados[i].strip().split(";")
        nomes.append(linha[0])
        valores.append(linha[1])

dados_ordenados = sorted(zip(nomes, valores), key=lambda x: x[1], reverse=True)

top_50 = dados_ordenados[:50]

x_top_50, y_top_50 = zip(*top_50)

plt.bar(x_top_50, y_top_50)

plt.xticks(rotation=45, ha="right")
plt.yticks([])
plt.ylabel("Valores")
plt.xlabel("Ações")
plt.title("Valores das 50 maiores ações")

plt.tight_layout()
plt.show()
