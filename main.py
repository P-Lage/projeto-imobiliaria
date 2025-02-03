# Importando os dados

import pandas as pd

# .read_csv() retorna a leitura dos arquivos de texto que contém dados separados por vírgulas
url = 'https://raw.githubusercontent.com/alura-cursos/pandas-conhecendo-a-biblioteca/main/base-de-dados/aluguel.csv'
dados = pd.read_csv(url, sep=';')

"""
Visualização dos dados:

# .head() retorna as primeiras linhas da base, sendo o parâmetro nulo = 5 primeira linhas
print(dados.head())

# .tail() retorna as últimas linhas da base, sendo o parâmetro nulo = 5 primeira linhas
print(dados.tail())

# type() verifica o tipo de dados da variável
type(dados)

Explorando as características gerais dos dados:

print(dados.shape)
print(dados.columns)
print(dados.info())
print(dados['Tipo'])
print(dados[['Quartos', 'Valor']])

"""

# Realizando a análise exploratória dos dados

colunasIniciais = dados.head()
print(colunasIniciais)

## Arredondamento dos valores com round

round(dados['Valor'].mean(), 2)

# Método goupby()
## Passando a coluna Tipo para a partir dela agrupar os dados
## numeric_only=True para a média ser feita só nos valores numéricos

round(dados.groupby('Tipo').mean(numeric_only=True), 2)

## numeric_only=True excluído pois não há mais necessidade

## Colchete duplo para criar um dataframe
## sortt_values('coluna') para organizar os valores do menor para o maior
round(dados.groupby('Tipo')[['Valor']].mean().sort_values('Valor'), 2)

# Criando um gráfico para a visualização

import matplotlib.pyplot as plt

df_preco_tipo = round(dados.groupby('Tipo')[['Valor']].mean().sort_values('Valor'), 2)
df_preco_tipo.plot(kind='barh', figsize=(14, 10), color = 'purple')
plt.show()