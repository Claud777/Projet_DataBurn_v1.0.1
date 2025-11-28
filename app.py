import streamlit as st
import pandas as pd

# Importações dos módulos atualizados
from modules.data_loader import load_multiple_years
from modules.ui import create_sidebar, filter_dataframe
from modules.graphs import (
    plot_line_evolution, 
    plot_bar_ranking, 
    plot_seasonal_volume, 
    plot_map_density, 
    plot_biome_distribution
)

# Configuração da página - tema claro
st.set_page_config(page_title="DataBurn Dashboard", layout="wide")
CURRENT_THEME = "plotly_white"
CURRENT_MAP = "carto-positron"

# sidebar e loading
anos_selecionados = create_sidebar()

if anos_selecionados:
    df_raw = load_multiple_years(anos_selecionados)
else:
    df_raw = None

# Título do Dashboard
st.title("DataBurn: Painel de Monitoramento de Queimadas")
st.markdown("---")

if df_raw is not None:
    # TRATAMENTO DE DADOS
    mapa_meses = {
        1: '01-Jan', 2: '02-Fev', 3: '03-Mar', 4: '04-Abr',
        5: '05-Mai', 6: '06-Jun', 7: '07-Jul', 8: '08-Ago',
        9: '09-Set', 10: '10-Out', 11: '11-Nov', 12: '12-Dez'
    }
    col_data = 'DataHora' 
    if col_data in df_raw.columns:
        df_raw[col_data] = pd.to_datetime(df_raw[col_data], errors='coerce')
        df_raw['Ano'] = df_raw[col_data].dt.year
        df_raw['Mes_Num'] = df_raw[col_data].dt.month
        df_raw['Mes_Nome'] = df_raw['Mes_Num'].map(mapa_meses)
    else:
        # A2: Melhorando o tratamento de data ausente
        df_raw['Ano'] = df_raw['ano_origem']
        df_raw['Mes_Num'] = 0 # Valor numérico para evitar erros de tipo
        df_raw['Mes_Nome'] = 'N/A' # Mantém N/A para visualização

    col_estado = 'Estado'; col_cidade = 'Municipio'; col_fogo = 'RiscoFogo'; col_chuva = 'Precipitacao'
    # Tratamento de valores ausentes/inválidos na coluna RiscoFogo
    # O valor -999.0 é um placeholder comum para dados ausentes/inválidos.
    if col_fogo in df_raw.columns:
        df_raw[col_fogo] = df_raw[col_fogo].replace(-999.0, pd.NA).astype('Float64')
        
    df_filtered = filter_dataframe(df_raw, col_estado, col_cidade)

    # BLOCO 1: ANÁLISE TEMPORAL
    st.header("1. Comportamento Temporal")
    
    # Configurações de Agrupamento
    tipo_view = st.radio("Visualizar evolução por:", ["Ano", "Mês"], horizontal=True)
    col_tempo = "Ano" if tipo_view == "Ano" else "Mes_Nome"
    # df_sorted removido: a ordenação e agrupamento são feitos dentro da função plot_line_evolution

    # GRÁFICO 1.A: TENDÊNCIA (LINHA)
    st.subheader("Tendência de Risco")
    st.markdown("""
    > **O que é:** Mostra a média do risco de fogo ao longo do tempo.  
    > **Utilidade:** Permite identificar se a situação está piorando (linha subindo) ou melhorando (linha descendo) no período selecionado.
    """)
    if col_fogo in df_filtered.columns:
        fig_evolu = plot_line_evolution(
            df_filtered, x_col=col_tempo, y_col=col_fogo, 
            title=f"Evolução da Média de Risco ({tipo_view})", 
            template=CURRENT_THEME
        )
        st.plotly_chart(fig_evolu, use_container_width=True)
    
    st.divider()

    # GRÁFICO 1.B: VOLUME (SAZONALIDADE)
    st.subheader("Volume Sazonal")
    st.markdown("""
    > **O que é:** Contagem total de focos de incêndio por período.  
    > **Utilidade:** Revela os meses de pico, ajudando a planejar ações preventivas antes da época crítica.
    """)
    if 'Mes_Nome' in df_filtered.columns:
        # Removendo ordenação redundante (df_sazonal)
        fig_saz = plot_seasonal_volume(
            df_filtered, time_col="Mes_Nome", 
            title="Total de Focos por Mês (Sazonalidade)", 
            template=CURRENT_THEME
        )
        st.plotly_chart(fig_saz, use_container_width=True)

    st.markdown("---")

    # BLOCO 2: RANKINGS
    st.header("2. Áreas Críticas (Rankings)")
    st.markdown("Comparativo entre as cidades com maiores índices de risco versus precipitação (chuva).")

    col_rank1, col_rank2 = st.columns(2)
    
    with col_rank1:
        if col_fogo in df_filtered.columns:
            fig_risk = plot_bar_ranking(
                df_filtered, cat_col=col_cidade, val_col=col_fogo,
                title="Top 10 Cidades: Risco de Fogo", 
                color_seq="Reds", is_percent=True, template=CURRENT_THEME
            )
            st.plotly_chart(fig_risk, use_container_width=True)

    with col_rank2:
        if col_chuva in df_filtered.columns:
            fig_rain = plot_bar_ranking(
                df_filtered, cat_col=col_cidade, val_col=col_chuva,
                title="Top 10 Cidades: Precipitação (Chuva)", 
                color_seq="Blues", is_percent=False, template=CURRENT_THEME
            )
            st.plotly_chart(fig_rain, use_container_width=True)

    st.markdown("---")

    # BLOCO 3: GEOESPACIAL E AMBIENTAL
    st.header("3. Análise Geográfica e Ambiental")
    
	    col_geo, col_legenda, col_bio = st.columns([2, 0.5, 1])
    
    with col_geo:
        st.subheader("Mapa de Calor")
        st.markdown("""
        **Utilidade:** Identifica visualmente as "Zonas Quentes" no território.  
        """)
	        if 'Latitude' in df_filtered.columns:
	            # Calcula min/max de FRP para a legenda
	            if 'FRP' in df_filtered.columns:
	                frp_data = df_filtered['FRP'].dropna()
	                frp_min = frp_data.min() if not frp_data.empty else 0
	                frp_max = frp_data.max() if not frp_data.empty else 0
	            else:
	                frp_min = 0
	                frp_max = 0
	
	            # Gera o mapa PyDeck
	            deck_map = plot_map_density(
	                df_filtered, 'Latitude', 'Longitude', frp_min=frp_min, frp_max=frp_max
	            )
	            st.pydeck_chart(deck_map, use_container_width=True)
	        else:
	            st.warning("Sem coordenadas GPS.")
	
	    with col_legenda:
	        st.subheader("Intensidade")
	        
	        # Legenda Vertical Simples
	        st.markdown(f"""
	        <div style="display: flex; flex-direction: column; align-items: center; height: 300px; justify-content: space-between;">
	            <div style="font-weight: bold; color: red;">ALTO ({frp_max:.1f})</div>
	            <div style="width: 20px; height: 200px; background: linear-gradient(to top, yellow, orange, red); border: 1px solid #333;"></div>
	            <div style="font-weight: bold; color: orange;">MÉDIO</div>
	            <div style="font-weight: bold; color: yellow;">BAIXO ({frp_min:.1f})</div>
	        </div>
	        """, unsafe_allow_html=True)
	
	    with col_bio:
        st.subheader("Biomas Afetados")
        st.markdown("""
        **Utilidade:** Mostra qual ecossistema está sofrendo mais impacto proporcionalmente.
        """)
        if 'Bioma' in df_filtered.columns:
            fig_bio = plot_biome_distribution(
                df_filtered, 'Bioma', template=CURRENT_THEME
            )
            st.plotly_chart(fig_bio, use_container_width=True)

    # TABELA FINAL
    with st.expander("Ver Tabela de Dados Completa"):
        st.dataframe(df_filtered, use_container_width=True)

else:
    st.info("Por favor, selecione os anos na barra lateral para carregar os dados.")