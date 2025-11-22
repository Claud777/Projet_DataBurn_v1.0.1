import plotly.express as px
import pandas as pd
import pydeck as pdk
import streamlit as st

# Configuração Global de Fontes
FONT_CONFIG = dict(family="Arial", size=14, color="#333333")

def plot_line_evolution(df, x_col, y_col, title, color_hex="#E25822", template="plotly_white"):
    """Gera gráfico de linha"""
    try:
        df_grouped = df.groupby(x_col, sort=False)[y_col].mean().reset_index()
    except Exception as e:
        st.error(f"Erro ao agrupar: {e}")
        return None

    fig = px.line(
        df_grouped, x=x_col, y=y_col, title=f"<b>{title}</b>", markers=True
    )
    
    fig.update_traces(line_color=color_hex, line_width=4, marker_size=8)
    
    fig.update_layout(
        hovermode="x unified",
        template=template,
        font=FONT_CONFIG,
        xaxis=dict(
            title=dict(text="<b>Período</b>", font=dict(size=16, color="black")),
            tickfont=dict(size=14, color="black"),
            showgrid=True, gridcolor="#e5e5e5"
        ),
        yaxis=dict(
            title=dict(text="<b>Média Registrada</b>", font=dict(size=16, color="black")),
            tickfont=dict(size=14, color="black"),
            showgrid=True, gridcolor="#e5e5e5"
        )
    )
    
    if pd.api.types.is_numeric_dtype(df_grouped[x_col]):
        fig.update_xaxes(dtick=1, tickformat="d")
        
    return fig

def plot_bar_ranking(df, cat_col, val_col, title, top_n=10, color_seq="Blues", is_percent=False, template="plotly_white"):
    """Gera ranking horizontal."""
    df_grouped = df.groupby(cat_col)[val_col].mean().reset_index()
    
    if is_percent:
        df_grouped[val_col] = df_grouped[val_col] * 100
        formato = '.1f'
    else:
        formato = '.2f'

    df_top = df_grouped.sort_values(by=val_col, ascending=True).tail(top_n)

    fig = px.bar(
        df_top, x=val_col, y=cat_col, title=f"<b>{title}</b>",
        text_auto=formato, orientation='h',
        color=val_col, color_continuous_scale=color_seq 
    )

    fig.update_layout(
        xaxis_title="<b>Valor</b>",
        yaxis_title="<b>Local</b>",
        template=template,
        coloraxis_showscale=False,
        height=400 + (top_n * 30),
        font=FONT_CONFIG
    )
    
    # Formatação do texto
    text_fmt = '<b>%{x:.1f}%</b>' if is_percent else '<b>%{x:.2f}</b>'
    
    fig.update_traces(
        texttemplate=text_fmt, 
        textposition="outside",
        textfont=dict(size=14, color="black")
    )

    return fig

def plot_seasonal_volume(df, time_col, title, color_seq="Reds", template="plotly_white"):
    """
    Gráfico de Sazonalidade.
    """
    df_grouped = df.groupby(time_col, sort=False).size().reset_index(name='Quantidade de Focos')
    
    fig = px.bar(
        df_grouped, x=time_col, y='Quantidade de Focos',
        title=f"<b>{title}</b>", color='Quantidade de Focos',
        color_continuous_scale=color_seq, text_auto=True
    )
    
    fig.update_layout(
        template=template,
        coloraxis_showscale=False,
        hovermode="x unified",
        font=FONT_CONFIG,
        xaxis=dict(title=dict(text="<b>Período</b>", font=dict(size=16))),
        yaxis=dict(title=dict(text="<b>Total de Focos</b>", font=dict(size=16)))
    )
    
    fig.update_traces(
        textfont=dict(size=14, color="black", family="Arial Black"), # Negrito forte
        textposition="outside"
    )
    return fig

def plot_map_density(df, lat_col, lon_col, map_style=None):
    """
    Gera um mapa otimizado usando PyDeck (WebGL).
    Substituindo o Plotly Density para evitar estouro de memória.
    """

    limit = 20000
    if len(df) > limit:
        data = df.sample(n=limit)
    else:
        data = df

    # Ajuste de peso (Intensidade)
    if 'FRP' in data.columns:
        data['FRP'] = data['FRP'].fillna(1) # Garante que não tem NaN
    else:
        data['FRP'] = 1

    # Define o ponto inicial da câmera (Centralizado no Maranhão)
    view_state = pdk.ViewState(
        latitude=-5.0,
        longitude=-45.0,
        zoom=5,
        pitch=0 # Inclinação 0 para ver de cima (como mapa tradicional)
    )

    # Camada de Calor (Heatmap) otimizada
    layer = pdk.Layer(
        "HeatmapLayer",
        data=data,
        get_position=[lon_col, lat_col],
        get_weight="FRP", # Peso baseado na intensidade do fogo
        opacity=0.6,
        radius_pixels=40, # Raio da mancha
        intensity=1,
        threshold=0.05,
    )

    # Renderização
    # map_style='light' usa o mapa claro padrão do PyDeck
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="light", # Força mapa claro para combinar com o tema
        tooltip={"text": "Concentração de Focos"}
    )
    
    return deck

def plot_biome_distribution(df, biome_col, template="plotly_white"):
    """Gráfico de Rosca."""
    df_grouped = df.groupby(biome_col).size().reset_index(name='Contagem')
    
    fig = px.pie(
        df_grouped, names=biome_col, values='Contagem', hole=0.5,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    fig.update_layout(
        template=template,
        legend_title="<b>Bioma</b>",
        height=400,
        font=FONT_CONFIG
    )
    
    fig.update_traces(
        textinfo='percent+label',
        textfont=dict(size=15, color="white"), 
        marker=dict(line=dict(color='#000000', width=1)) 
    )
    
    return fig