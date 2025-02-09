# Importando os dados

import matplotlib.pyplot as plt
import pandas as pd

# .read_csv() retorna a leitura dos arquivos de texto que contém dados separados por vírgulas
url = 'https://raw.githubusercontent.com/alura-cursos/pandas-conhecendo-a-biblioteca/main/base-de-dados/aluguel.csv'
dados = pd.read_csv(url, sep=';')
print(dados)

#Visualização dos dados:

# .head() retorna as primeiras linhas da base, sendo o parâmetro nulo = 5 primeira linhas
print(dados.head())

# .tail() retorna as últimas linhas da base, sendo o parâmetro nulo = 5 primeira linhas
print(dados.tail())

# type() verifica o tipo de dados da variável
type(dados)

# Explorando as características gerais dos dados:

print(dados.shape)
print(dados.columns)
print(dados.info())
print(dados['Tipo'])
print(dados[['Quartos', 'Valor']])


# Realizando a análise exploratória dos dados

colunasIniciais = dados.head()
print(colunasIniciais)

# Arredondamento dos valores com round

round(dados['Valor'].mean(), 2)

# Método goupby()
# Passando a coluna Tipo para a partir dela agrupar os dados
# numeric_only=True para a média ser feita só nos valores numéricos

round(dados.groupby('Tipo').mean(numeric_only=True), 2)

# numeric_only=True excluído pois não há mais necessidade

# Colchete duplo para criar um dataframe
# sortt_values('coluna') para organizar os valores do menor para o maior
round(dados.groupby('Tipo')[['Valor']].mean().sort_values('Valor'), 2)

# Criando um gráfico para a visualização

df_preco_tipo = round(dados.groupby(
    'Tipo')[['Valor']].mean().sort_values('Valor'), 2)
df_preco_tipo.plot(kind='barh', figsize=(14, 10), color='purple')
plt.show()


# Removendo os imóveis comerciais

# repr retorna a representação "oficial" do NumPy
repr(dados.Tipo.unique())

# Criando um array somente com imóveis comerciais
imoveis_comerciais = ['Conjunto Comercial/Sala',
                      'Prédio Inteiro', 'Loja/Salão',
                      'Galpão/Depósito/Armazém',
                      'Casa Comercial', 'Terreno Padrão',
                      'Loja Shopping/ Ct Comercial',
                      'Box/Garagem', 'Chácara',
                      'Loteamento/Condomínio', 'Sítio',
                      'Pousada/Chalé', 'Hotel', 'Indústria']

# DataFrame com imóveis comerciais
dados.query('@imoveis_comerciais in Tipo')

# DataFrame sem imóveis comerciais
dados.query('@imoveis_comerciais not in Tipo')

df = dados.query('@imoveis_comerciais not in Tipo')
df.head()

repr(df.Tipo.unique())

df_preco_tipo = round(df.groupby(
    'Tipo')[['Valor']].mean().sort_values('Valor'), 2)
df_preco_tipo.plot(kind='barh', figsize=(14, 10), color='purple')
plt.show()


# Determinando o percentual de cada tipo de imóvel

## .value_counts() Retorna uma series com os valores referentes à coluna
df.Tipo.value_counts()

## Retorna a mesma series só que em porcentagem
df.Tipo.value_counts(normalize=True)

## .to_frame() converte para um DataFram
df_percentual_tipo = df.Tipo.value_counts(normalize=True).to_frame()
print(df_percentual_tipo)

## Alterando o nome da  coluna proportion para percentual

df_percentual_tipo.rename(columns={'proportion': 'Percentuais'}, inplace=True)

df_percentual_tipo = df_percentual_tipo.sort_values('Percentuais')

df_percentual_tipo.plot(kind='bar', figsize=(14, 10), color='green', xlabel = 'Tipos', ylabel = 'Percentual')
plt.show()

## Selecionando apenas apartamentos

df = df.query("Tipo == 'Apartamento'")
df.head()

## Tratando dados nulos

df.isnull()

## .sum() retorna a soma dos valores nulos
df.isnull().sum()

## .fillna(0) preenche os valores nulos com 0
df = df.fillna(0)
df.isnull().sum()
## .dropna() exclui as linhas com valores nulos
## .interpolate() preenche os valores nulos com a média dos valores anteriores e posteriores

# Removendo registros com valores nulos

registros_a_remover = df.query('Valor == 0 or Condominio == 0').index

df.drop(registros_a_remover, axis=0, inplace=True)

df.query('Valor == 0 or Condominio == 0').index

df.Tipo.unique()

df.drop(['Tipo'], axis=1, inplace=True)

df.head()

# Aplicando filtros

selecao_1 = df['Quartos'] == 1
df[selecao_1]

selecao_2 = df['Valor'] < 1200
df[selecao_2]

selecao_final = (selecao_1) & (selecao_2)
df_1 = df[selecao_final]

selecao_3 = (df['Quartos'] >= 2) & (df['Valor'] < 3000) & (df['Area'] > 70)
df_2 = df[selecao_3]

# Salvando os dados

df.to_csv('dados_apartamentos.csv', sep=';', index=False)
pd.read_csv('dados_apartamentos.csv', sep=';')

df_1.to_csv('dados_apartamentos_1.csv', sep=';', index=False)
pd.read_csv('dados_apartamentos_1.csv', sep=';')

df_2.to_csv('dados_apartamentos_2.csv', sep=';', index=False)
pd.read_csv('dados_apartamentos_2.csv', sep=';')

# Criando colunas numéricas

url = 'https://raw.githubusercontent.com/alura-cursos/pandas-conhecendo-a-biblioteca/main/base-de-dados/aluguel.csv'
dados = pd.read_csv(url, sep=';')
dados.head()

dados['Valor_por_mes'] = dados['Valor'] + dados['Condominio']
dados.head()

dados['Valor_por_ano'] = dados['Valor_por_mes'] * 12 + dados['IPTU']
dados.head()

# Criando colunas categóricas

dados['Descrição'] = dados['Tipo'] + ', ' + dados['Bairro']
dados.head()

dados['Descrição'] = dados['Tipo'] + ' em ' + dados['Bairro'] + ' com ' + \
        (dados['Quartos']).astype(str) + ' quarto(s) e ' + \
        dados['Vagas'].astype(str) + ' vaga(s) de garagem.'
dados.head()

# Criando colunas binárias

dados['Possui suites'] = dados['Suites'].apply(lambda x: 'Sim' if x > 0 else 'Não')
dados.head()

dados.to_csv('dados_completos.csv', sep=';', index=False)
pd.read_csv('dados_completos.csv', sep=';')