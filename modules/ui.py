import streamlit as st

def create_sidebar():
    """Cria a sidebar e retorna os anos selecionados"""
    st.sidebar.title("Filtros para análise")
    
    anos_disponiveis = [2020, 2021, 2022, 2023, 2024, 2025]
    anos_selecionados = st.sidebar.multiselect(
        "Selecione os Anos:", 
        options=anos_disponiveis, 
        default=[2020]
    )
    return anos_selecionados

def filter_dataframe(df, col_estado, col_cidade):
    """Aplica os filtros de Estado e Cidade e retorna o DF filtrado"""
    st.sidebar.markdown("---")
    st.sidebar.header("Localização")
    
    df_filtered = df.copy()
    colunas_presentes = df.columns.tolist()

    # Filtro de Estado
    if col_estado in colunas_presentes:
        lista_estados = sorted(df[col_estado].dropna().unique())
        estado_sel = st.sidebar.selectbox("Filtrar Estado:", ["Todos"] + lista_estados)
        
        if estado_sel != "Todos":
            df_filtered = df_filtered[df_filtered[col_estado] == estado_sel]
    
    # Filtro de Cidade
    if col_cidade in colunas_presentes:
        lista_cidades = sorted(df_filtered[col_cidade].dropna().unique())
        cidade_sel = st.sidebar.selectbox("Filtrar Cidade:", ["Todas"] + lista_cidades)
        
        if cidade_sel != "Todas":
            df_filtered = df_filtered[df_filtered[col_cidade] == cidade_sel]
            
    return df_filtered