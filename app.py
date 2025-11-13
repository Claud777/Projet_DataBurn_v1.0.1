import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(
    page_title="DataBurn Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🔥 DataBurn: Análise de Big Data")

st.markdown("""
Esta é a estrutura inicial do dashboard para a análise de Big Data.
O objetivo é apresentar os dados obtidos e identificar as causas de um problema específico.
O time de front-end pode usar esta estrutura para desenvolver o design.
""")

# Carregar dados de exemplo (usando o primeiro arquivo encontrado)
data_path = "data/db_2020/dados_2020.csv"
try:
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        st.header("Amostra de Dados (2020)")
        st.dataframe(df.head())
    else:
        st.warning(f"Arquivo de dados não encontrado: {data_path}")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")

# Seção para a análise
st.header("Resultados da Análise")
st.info("Esta seção será preenchida com gráficos, métricas e a conclusão da análise para identificar a causa do problema.")

# Placeholder para o time de front-end
st.sidebar.title("Configurações e Filtros")
st.sidebar.markdown("Use esta barra lateral para adicionar filtros de data, região, etc.")

st.sidebar.header("Status do Projeto")
st.sidebar.metric("Dados Carregados", "Sim")
st.sidebar.metric("Estrutura Streamlit", "Pronta")

st.caption("Desenvolvido para o projeto DataBurn.")
