# Importando bibliotecas necessárias
import matplotlib.pyplot as plt
import pandas as pd

# ------------------------------
# 1. CARREGAMENTO DOS DADOS
# ------------------------------

# Define a URL do dataset e carrega os dados em um DataFrame
url = 'https://raw.githubusercontent.com/alura-cursos/pandas-conhecendo-a-biblioteca/main/base-de-dados/aluguel.csv'
dados = pd.read_csv(url, sep=';')

# Exibe as primeiras e últimas linhas para inspeção inicial
print("Primeiras 5 linhas do dataset:")
print(dados.head())
print("\nÚltimas 5 linhas do dataset:")
print(dados.tail())

# ------------------------------
# 2. ANÁLISE EXPLORATÓRIA INICIAL
# ------------------------------

print("\nDimensões do DataFrame (linhas, colunas):", dados.shape)
print("\nNomes das colunas:", dados.columns.tolist())
print("\nTipos de dados e informações gerais:")
print(dados.info())

# Análise estatística básica da coluna 'Valor'
media_valor = round(dados['Valor'].mean(), 2)
print(f"\nMédia dos valores de aluguel: R$ {media_valor}")

# Agrupa dados por tipo de imóvel e calcula médias numéricas
media_por_tipo = round(dados.groupby('Tipo').mean(numeric_only=True), 2)
print("\nMédia de valores por tipo de imóvel:")
print(media_por_tipo[['Valor']].sort_values('Valor'))

# Gera gráfico de barras horizontal para visualização
df_preco_tipo = round(dados.groupby('Tipo')[['Valor']].mean().sort_values('Valor'), 2)
df_preco_tipo.plot(kind='barh', figsize=(14, 10), color='purple', title='Média de Valores por Tipo de Imóvel')
plt.show()

# ------------------------------
# 3. LIMPEZA E FILTRAGEM DE DADOS
# ------------------------------

# Define tipos de imóveis comerciais a serem removidos
imoveis_comerciais = [
    'Conjunto Comercial/Sala', 'Prédio Inteiro', 'Loja/Salão',
    'Galpão/Depósito/Armazém', 'Casa Comercial', 'Terreno Padrão',
    'Loja Shopping/ Ct Comercial', 'Box/Garagem', 'Chácara',
    'Loteamento/Condomínio', 'Sítio', 'Pousada/Chalé', 'Hotel', 'Indústria'
]

# Filtra DataFrame para manter apenas imóveis residenciais
df_residencial = dados.query('Tipo not in @imoveis_comerciais')
print("\nTipos de imóveis após remoção dos comerciais:")
print(df_residencial['Tipo'].unique())

# Remove registros com valores inválidos (Valor ou Condomínio = 0)
registros_invalidos = df_residencial.query('Valor == 0 or Condominio == 0').index
df_residencial.drop(registros_invalidos, axis=0, inplace=True)

# ------------------------------
# 4. ANÁLISE DE DISTRIBUIÇÃO
# ------------------------------

# Calcula percentual de cada categoria
df_percentual = df_residencial['Tipo'].value_counts(normalize=True).to_frame()
df_percentual.columns = ['Percentual']

# Gerar gráfico com os dados
df_percentual.sort_values('Percentual').plot(kind='bar', figsize=(14, 10), color='green',
                                            title='Distribuição Percentual por Categoria')
plt.show()


# ------------------------------
# 5. APLICAÇÃO DE FILTROS
# ------------------------------

# Filtro 1: Apartamentos com 1 quarto e valor < R$ 1200
filtro_1 = (df_residencial['Quartos'] == 1) & (df_residencial['Valor'] < 1200)
df_filtro1 = df_residencial[filtro_1]

# Filtro 2: Imóveis com 2+ quartos, valor < R$ 3000 e área > 70m²
filtro_2 = (df_residencial['Quartos'] >= 2) & (df_residencial['Valor'] < 3000) & (df_residencial['Area'] > 70)
df_filtro2 = df_residencial[filtro_2]

# ------------------------------
# 6. CRIAÇÃO DE NOVAS COLUNAS
# ------------------------------

# Calcula custo total mensal (aluguel + condomínio)
df_residencial['Custo_Mensal'] = df_residencial['Valor'] + df_residencial['Condominio']

# Calcula custo anual total (incluindo IPTU)
df_residencial['Custo_Anual'] = (df_residencial['Custo_Mensal'] * 12) + df_residencial['IPTU']

# Cria descrição textual para cada imóvel
df_residencial['Descricao'] = (
    df_residencial['Tipo'] + ' em ' + df_residencial['Bairro'] + 
    ' com ' + df_residencial['Quartos'].astype(str) + 
    ' quarto(s) e ' + df_residencial['Vagas'].astype(str) + ' vaga(s).'
)

# Cria coluna binária indicando presença de suíte
df_residencial['Tem_Suite'] = df_residencial['Suites'].apply(lambda x: 'Sim' if x > 0 else 'Não')

# ------------------------------
# 7. SALVAMENTO DOS RESULTADOS
# ------------------------------

# Salva DataFrames processados em arquivos CSV
df_residencial.to_csv('dados_residenciais.csv', sep=';', index=False)
df_filtro1.to_csv('filtro_apartamentos_economicos.csv', sep=';', index=False)
df_filtro2.to_csv('filtro_imoveis_premium.csv', sep=';', index=False)

print("\nProcesso concluído. Arquivos salvos:")
print("- dados_residenciais.csv\n- filtro_apartamentos_economicos.csv\n- filtro_imoveis_premium.csv")