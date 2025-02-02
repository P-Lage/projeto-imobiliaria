# Importando os dados

import pandas as pd

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

"""
