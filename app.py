import streamlit as st
import pandas as pd

# Importando os módulos
from modules.data_loader import load_multiple_years
from modules.utils import formatar_numero
from modules.ui import create_sidebar, filter_dataframe
from modules.graphs import plot_line_evolution, plot_bar_ranking

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
    # MAPEAMENTO DE COLUNAS
    col_estado = 'Estado'      
    col_cidade = 'Municipio'    
    col_fogo = 'RiscoFogo'     
    col_chuva = 'Precipitacao'  
    # Determina coluna de tempo, caso não exista 'mes', usa 'ano_origem'
    col_tempo = 'mes' if 'mes' in df_raw.columns else 'ano_origem' 

    # Aplica filtros
    df_filtered = filter_dataframe(df_raw, col_estado, col_cidade)

    # KPIs
    st.subheader(f"Análise Consolidada")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    media_fogo = df_filtered[col_fogo].mean() if col_fogo in df_filtered.columns else 0
    total_chuva = df_filtered[col_chuva].sum() if col_chuva in df_filtered.columns else 0
    cidades_unicas = df_filtered[col_cidade].nunique() if col_cidade in df_filtered.columns else 0
    
    kpi1.metric("Registros Analisados", formatar_numero(len(df_filtered)))
    kpi2.metric("Média Risco de Fogo", formatar_numero(media_fogo, 2))
    kpi3.metric("Precipitação Total", formatar_numero(total_chuva, 2))
    kpi4.metric("Cidades Atingidas", cidades_unicas)

    st.markdown("---")

    # GRÁFICOS
    st.subheader("Visualização dinâmica de Dados")
    
    # Gráfico de Evolução (Linha)
    if col_fogo in df_filtered.columns:
        st.markdown("##### Evolução do Risco de Fogo")
        fig_evolu = plot_line_evolution(
            df_filtered, 
            x_col=col_tempo, 
            y_col=col_fogo, 
            title=f"Média de Risco de Fogo por {col_tempo.capitalize()}",
            color_hex="#FF4B4B" # Vermelho remetendo ao fogo
        )
        if fig_evolu:
            st.plotly_chart(fig_evolu, use_container_width=True)
    
    # Gráficos Comparativos (Colunas)
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Ranking de Cidades com maior risco
        if col_cidade in df_filtered.columns and col_fogo in df_filtered.columns:
            fig_rank = plot_bar_ranking(
                df_filtered, 
                cat_col=col_cidade, 
                val_col=col_fogo, 
                title="Top 10 Cidades (Maior Risco Médio)"
            )
            st.plotly_chart(fig_rank, use_container_width=True)
            
    with col_g2:
        # Comparação de Chuva (Ranking)
        if col_cidade in df_filtered.columns and col_chuva in df_filtered.columns:
            fig_rain = plot_bar_ranking(
                df_filtered,
                cat_col=col_cidade,
                val_col=col_chuva,
                title="Top 10 Cidades (Maior Precipitação)",
            )
            # Ajuste de cor para azul (remete a chuva)
            fig_rain.update_traces(marker_color="#0083B8") 
            st.plotly_chart(fig_rain, use_container_width=True)

    st.markdown("---")

    # Tabela
    with st.expander("Ver Base de Dados Filtrada"):
        st.dataframe(df_filtered.head(100), use_container_width=True)

else:
    st.info("Selecione um ano para começar.")