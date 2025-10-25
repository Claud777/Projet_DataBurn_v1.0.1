# analise_queimadas.py
# Descrição: Análise exploratória de dados sobre queimadas no estado do Maranhão
# Bibliotecas: pandas, matplotlib, seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração estética do seaborn
sns.set(style="whitegrid", palette="Set2")

# Caminho do arquivo CSV
CAMINHO_CSV = "../data/queimadas_ma.csv"

# Diretórios de saída
DIR_RESULTADOS = "../results"
DIR_GRAFICOS = os.path.join(DIR_RESULTADOS, "graphs")

os.makedirs(DIR_GRAFICOS, exist_ok=True)

print("🔍 Carregando base de dados...")
df = pd.read_csv(CAMINHO_CSV)

print("\n✅ Base carregada com sucesso!")
print(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")

# Exibir as primeiras linhas
print("\n📄 Visualização inicial:")
print(df.head())

# Informações gerais
print("\nℹ️ Informações da base:")
print(df.info())

# Estatísticas descritivas
print("\n📊 Estatísticas descritivas:")
print(df.describe(include='all'))

# Verificar valores nulos
print("\n🚨 Valores nulos por coluna:")
print(df.isnull().sum())

# Exemplo de colunas comuns (você pode ajustar conforme o seu CSV)
# Vamos supor que temos colunas como: "estado", "municipio", "ano", "mes", "numero_queimadas"
# Caso tenha outro nome, você pode adaptar aqui.

if "ano" in df.columns and "municipio" in df.columns:
    # Queimadas por ano
    queimadas_por_ano = df.groupby("ano").size()
    queimadas_por_ano.plot(kind="bar", figsize=(10, 5))
    plt.title("Número de queimadas por ano - Maranhão")
    plt.xlabel("Ano")
    plt.ylabel("Número de ocorrências")
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_GRAFICOS, "queimadas_por_ano.png"))
    plt.close()

    # Queimadas por mês (se houver coluna 'mes')
    if "mes" in df.columns:
        queimadas_por_mes = df.groupby("mes").size().sort_index()
        queimadas_por_mes.plot(kind="bar", figsize=(10, 5), color="orange")
        plt.title("Número de queimadas por mês - Maranhão")
        plt.xlabel("Mês")
        plt.ylabel("Número de ocorrências")
        plt.tight_layout()
        plt.savefig(os.path.join(DIR_GRAFICOS, "queimadas_por_mes.png"))
        plt.close()

    # Top 10 municípios
    top_municipios = df["municipio"].value_counts().head(10)
    top_municipios.plot(kind="bar", figsize=(10, 5), color="green")
    plt.title("Top 10 municípios com mais queimadas")
    plt.xlabel("Município")
    plt.ylabel("Número de ocorrências")
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_GRAFICOS, "top10_municipios.png"))
    plt.close()

print("\n📂 Gráficos salvos em:", DIR_GRAFICOS)

# Salvar estatísticas em arquivo
with open(os.path.join(DIR_RESULTADOS, "estatisticas.txt"), "w", encoding="utf-8") as f:
    f.write("Resumo da Análise de Queimadas no Maranhão\n")
    f.write("=" * 50 + "\n\n")
    f.write(str(df.describe(include='all')))
    f.write("\n\nValores nulos por coluna:\n")
    f.write(str(df.isnull().sum()))
    f.write("\n\nTop 10 municípios com mais queimadas:\n")
    f.write(str(top_municipios))

print("\n📑 Estatísticas salvas com sucesso!")
