import streamlit as st
import pandas as pd

from modules.data_loader import load_multiple_years
from modules.utils import formatar_numero
from modules.ui import create_sidebar, filter_dataframe
# Importação completa das funções gráficas
from modules.graphs import (
    plot_line_evolution, 
    plot_bar_ranking, 
    plot_seasonal_volume, 
    plot_map_density, 
    plot_biome_distribution
)

# Configuração da página
st.set_page_config(page_title="DataBurn Dashboard", layout="wide")

# Sidebar e Carregamento de Dados
anos_selecionados = create_sidebar()

if anos_selecionados:
    df_raw = load_multiple_years(anos_selecionados)
else:
    df_raw = None

# Título Principal
st.title("DataBurn: Painel de Monitoramento")

if df_raw is not None:
    # Tratamento de Datas e Meses
    mapa_meses = {
        1: '01 - Janeiro', 2: '02 - Fevereiro', 3: '03 - Março', 4: '04 - Abril',
        5: '05 - Maio', 6: '06 - Junho', 7: '07 - Julho', 8: '08 - Agosto',
        9: '09 - Setembro', 10: '10 - Outubro', 11: '11 - Novembro', 12: '12 - Dezembro'
    }
    
    col_data_nome = 'DataHora' 
    
    if col_data_nome in df_raw.columns:
        # Converte e extrai informações de data
        df_raw[col_data_nome] = pd.to_datetime(df_raw[col_data_nome], errors='coerce')
        df_raw['Ano'] = df_raw[col_data_nome].dt.year
        df_raw['Mes_Num'] = df_raw[col_data_nome].dt.month
        df_raw['Mes_Nome'] = df_raw['Mes_Num'].map(mapa_meses)
    else:
        df_raw['Ano'] = df_raw['ano_origem']
        df_raw['Mes_Nome'] = 'N/A'

    # Mapeamento de Colunas
    col_estado = 'Estado'
    col_cidade = 'Municipio'
    col_fogo = 'RiscoFogo'
    col_chuva = 'Precipitacao'

    # Aplicação dos Filtros
    df_filtered = filter_dataframe(df_raw, col_estado, col_cidade)

    # Seção: Análise Temporal
    st.subheader("Análise Temporal e Sazonalidade")
    
    # Seletor de visualização (Ano vs Mês)
    tipo_visualizacao = st.radio(
        "Agrupar dados por:", 
        ["Ano", "Mês"], 
        horizontal=True
    )

    if tipo_visualizacao == "Ano":
        col_tempo_grafico = "Ano"
    else:
        if 'Mes_Nome' in df_filtered.columns and df_filtered['Mes_Nome'].iloc[0] != 'N/A':
            col_tempo_grafico = "Mes_Nome"
        else:
            col_tempo_grafico = "Ano"

    col_evo, col_saz = st.columns(2)

    with col_evo:
        # Gráfico de Linha (Tendência Média)
        if col_fogo in df_filtered.columns:
            fig_evolu = plot_line_evolution(
                df_filtered.sort_values(by="Mes_Nome" if col_tempo_grafico == "Mes_Nome" else "Ano"), 
                x_col=col_tempo_grafico, 
                y_col=col_fogo, 
                title=f"Evolução Média do Risco ({tipo_visualizacao})",
                color_hex="#FF4B4B"
            )
            st.plotly_chart(fig_evolu, use_container_width=True)

    with col_saz:
        # Gráfico de Volume Sazonal (Barras Coloridas)
        if 'Mes_Nome' in df_filtered.columns and df_filtered['Mes_Nome'].iloc[0] != 'N/A':
            # Ordena por mês para o gráfico ficar cronológico
            df_sazonal = df_filtered.sort_values(by="Mes_Nome")
            
            fig_sazonal = plot_seasonal_volume(
                df_sazonal,
                time_col="Mes_Nome",
                title="Volume Total de Queimadas por Mês",
                color_seq="Reds" 
            )
            st.plotly_chart(fig_sazonal, use_container_width=True)
        else:
            st.info("Dados mensais não disponíveis para gerar análise sazonal.")

    st.markdown("---")
    
    # Seção: Rankings Top 10
    col1, col2 = st.columns(2)
    with col1:
        if col_fogo in df_filtered.columns:
            fig_fogo = plot_bar_ranking(
                df_filtered,
                cat_col=col_cidade,
                val_col=col_fogo,
                title="Top 10 Cidades - Risco Crítico (%)",
                color_seq="Reds",
                is_percent=True
            )
            st.plotly_chart(fig_fogo, use_container_width=True)

    with col2:
        if col_chuva in df_filtered.columns:
            fig_chuva = plot_bar_ranking(
                df_filtered,
                cat_col=col_cidade,
                val_col=col_chuva,
                title="Top 10 Cidades - Maior Precipitação (mm)",
                color_seq="Blues",
                is_percent=False
            )
            st.plotly_chart(fig_chuva, use_container_width=True)

    st.markdown("---")
    
    # Seção: Análise Geoespacial e Ambiental
    st.subheader("Análise Geoespacial e Ambiental")

    # --- AQUI ESTAVA O ERRO: CORRIGIDO DE st.acolumns PARA st.columns ---
    col_map, col_bio = st.columns([2, 1])

    with col_map:
        st.markdown("##### Densidade de Focos de Calor")
        # Verifica se as colunas de lat/long existem
        if 'Latitude' in df_filtered.columns and 'Longitude' in df_filtered.columns:
            fig_map = plot_map_density(df_filtered, 'Latitude', 'Longitude')
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("Coordenadas geográficas não encontradas para gerar o mapa.")

    with col_bio:
        st.markdown("##### Distribuição por Bioma")
        # Verifica se a coluna Bioma existe
        col_bioma = 'Bioma' 
        if col_bioma in df_filtered.columns:
            fig_bio = plot_biome_distribution(df_filtered, col_bioma)
            st.plotly_chart(fig_bio, use_container_width=True)
        else:
            st.info("Dados de Bioma não disponíveis.")

    # Visualização da Tabela Bruta
    with st.expander("Visualização dados brutos filtrados"):
        st.dataframe(df_filtered, use_container_width=True)

else:
    st.info("Selecione os dados na barra lateral.")