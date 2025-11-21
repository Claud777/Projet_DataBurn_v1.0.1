import streamlit as st
import pandas as pd

from modules.data_loader import load_multiple_years
from modules.utils import formatar_numero
from modules.ui import create_sidebar, filter_dataframe
from modules.graphs import plot_line_evolution, plot_bar_ranking

#  Configuração
st.set_page_config(page_title="DataBurn Dashboard", layout="wide")

#  Sidebar e Dados
anos_selecionados = create_sidebar()

if anos_selecionados:
    df_raw = load_multiple_years(anos_selecionados)
else:
    df_raw = None

#  Título
st.title("DataBurn: Painel de Monitoramento")

if df_raw is not None:
    # TRATAMENTO DE DATAS E MESES
    #Traduz e ordena meses
    mapa_meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    # Tenta converter coluna de Data
    col_data_nome = 'DataHora'
    
    if col_data_nome in df_raw.columns:
        # Converte para datetime
        df_raw[col_data_nome] = pd.to_datetime(df_raw[col_data_nome], errors='coerce')
        # Cria coluna de Ano e Mês
        df_raw['Ano'] = df_raw[col_data_nome].dt.year
        df_raw['Mes_Num'] = df_raw[col_data_nome].dt.month
        df_raw['Mes_Nome'] = df_raw['Mes_Num'].map(mapa_meses)
    else:
        # Se não tiver data, usa o ano de origem
        df_raw['Ano'] = df_raw['ano_origem']
        df_raw['Mes_Nome'] = 'N/A'

    # MAPEAMENTO DE COLUNAS
    col_estado = 'Estado'
    col_cidade = 'Municipio'
    col_fogo = 'RiscoFogo'
    col_chuva = 'Precipitacao'

    # Aplica filtros
    df_filtered = filter_dataframe(df_raw, col_estado, col_cidade)

    #Seleção de view (ANO vs MÊS)
    st.subheader("Análise Temporal")
    
    # Botão de escolha
    tipo_visualizacao = st.radio(
        "Agrupar evolução por:", 
        ["Ano", "Mês"], 
        horizontal=True
    )

    # Define qual coluna usar no eixo X baseada na escolha
    if tipo_visualizacao == "Ano":
        col_tempo_grafico = "Ano"
    else:
        # Verifica se temos meses válidos
        if 'Mes_Nome' in df_filtered.columns and df_filtered['Mes_Nome'].iloc[0] != 'N/A':
            col_tempo_grafico = "Mes_Nome"
        else:
            st.warning("Dados mensais não disponíveis. Mostrando por Ano.")
            col_tempo_grafico = "Ano"

    # GRÁFICOS
    
    # Gráfico de Linha (Evolução)
    if col_fogo in df_filtered.columns:
        fig_evolu = plot_line_evolution(
            df_filtered.sort_values(by="Mes_Nome" if col_tempo_grafico == "Mes_Nome" else "Ano"), 
            x_col=col_tempo_grafico, 
            y_col=col_fogo, 
            title=f"Evolução do Risco de Fogo (Por {tipo_visualizacao})",
            color_hex="#FF4B4B"
        )
        st.plotly_chart(fig_evolu, use_container_width=True)

    st.markdown("---")
    
    # Rankings (Lado a Lado)
    col1, col2 = st.columns(2)
    
    with col1:
        if col_fogo in df_filtered.columns:
            # Risco de Fogo  Vermelho ("Reds") + Porcentagem (True)
            fig_fogo = plot_bar_ranking(
                df_filtered,
                cat_col=col_cidade,
                val_col=col_fogo,
                title="Top 10 Cidades - Maior Risco de Fogo (%)",
                color_seq="Reds",
                is_percent=True # Transforma 1.0 em 100%
            )
            st.plotly_chart(fig_fogo, use_container_width=True)

    with col2:
        if col_chuva in df_filtered.columns:
            # Chuva = Azul ("Blues") + Valor Absoluto (False)
            fig_chuva = plot_bar_ranking(
                df_filtered,
                cat_col=col_cidade,
                val_col=col_chuva,
                title="Top 10 Cidades - Maior Precipitação (mm)",
                color_seq="Blues",
                is_percent=False # Mantém número normal
            )
            st.plotly_chart(fig_chuva, use_container_width=True)

    #TABELA
    with st.expander("Ver Dados Detalhados"):
        st.dataframe(df_filtered, use_container_width=True)

else:
    st.info("Selecione os dados na barra lateral.")