import streamlit as st
import pandas as pd

# Importando os módulos
from modules.data_loader import load_multiple_years
from modules.utils import formatar_numero
from modules.ui import create_sidebar, filter_dataframe

# Configuração da Página
st.set_page_config(
    page_title="Dados de Monitoramento - DataBurn",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar e Carregamento
anos_selecionados = create_sidebar()

if anos_selecionados:
    df_raw = load_multiple_years(anos_selecionados)
else:
    df_raw = None

# Corpo Principal
st.title("DataBurn: Painel de Monitoramento")

if df_raw is not None:
    # Mapeamento (Lembra de manter os nomes corretos que ajustaste antes)
    col_estado = 'Estado'      
    col_cidade = 'Municipio'    
    col_fogo = 'RiscoFogo'     
    col_chuva = 'Precipitacao'  

    # Aplica filtros (Função que veio do modules/ui.py)
    df_filtered = filter_dataframe(df_raw, col_estado, col_cidade)

    # KPIs
    st.subheader(f"Análise Consolidada ({', '.join(map(str, anos_selecionados))})")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    # Cálculos
    media_fogo = df_filtered[col_fogo].mean() if col_fogo in df_filtered.columns else 0
    total_chuva = df_filtered[col_chuva].sum() if col_chuva in df_filtered.columns else 0
    cidades_unicas = df_filtered[col_cidade].nunique() if col_cidade in df_filtered.columns else 0
    
    # Exibição
    kpi1.metric("Registros Analisados", formatar_numero(len(df_filtered)))
    kpi2.metric("Média Risco de Fogo", formatar_numero(media_fogo, 2))
    kpi3.metric("Precipitação Total", formatar_numero(total_chuva, 2))
    kpi4.metric("Cidades Atingidas", cidades_unicas)

    st.markdown("---")

    # --- Tabela ---
    st.subheader("Base de Dados Filtrada")
    st.dataframe(df_filtered.head(50), use_container_width=True)

    # --- Rodapé Técnico ---
    st.markdown("---")
    with st.expander("🔧 Detalhes Técnicos (Dev Only)"):
        st.write(df_filtered.dtypes)

else:
    st.info("Selecione um ano para começar.")
