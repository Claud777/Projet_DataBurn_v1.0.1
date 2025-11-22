import plotly.express as px
import pandas as pd
import streamlit as st

def plot_line_evolution(df, x_col, y_col, title, color_hex="#FF4B4B", template="plotly_dark"):
    """
    Gera um gráfico de linha para visualizar a evolução temporal (média) de uma métrica.
    Ideal para analisar tendências ao longo de anos ou meses.
    """
    try:
        # Agrupa os dados pela média do período
        df_grouped = df.groupby(x_col)[y_col].mean().reset_index()
    except Exception as e:
        st.error(f"Erro ao agrupar dados: {e}")
        return None

    fig = px.line(
        df_grouped, 
        x=x_col, 
        y=y_col, 
        title=title,
        markers=True
    )
    
    fig.update_traces(line_color=color_hex, line_width=3)
    
    # Configuração visual dos eixos
    axis_color = "white" if "dark" in template else "#31333F"
    
    fig.update_layout(
        hovermode="x unified",
        template=template,
        xaxis=dict(
            title=dict(text="<b>Período</b>", font=dict(family="Arial Black", size=18, color=color_hex))
        ),
        yaxis=dict(
            title=dict(text="<b>Média</b>", font=dict(family="Arial Black", size=18, color=color_hex))
        )
    )
    
    # Formatação para anos inteiros (sem vírgula)
    if pd.api.types.is_numeric_dtype(df_grouped[x_col]):
        fig.update_xaxes(dtick=1, tickformat="d")
        
    return fig

def plot_bar_ranking(df, cat_col, val_col, title, top_n=10, color_seq="Blues", is_percent=False, template="plotly_dark"):
    """
    Gera um ranking horizontal (Top N) com gradiente de cor baseado no valor.
    Suporta formatação percentual ou absoluta.
    """
    df_grouped = df.groupby(cat_col)[val_col].mean().reset_index()
    
    # Ajuste para visualização em porcentagem (0-1 -> 0-100%)
    if is_percent:
        df_grouped[val_col] = df_grouped[val_col] * 100
        formato = '.1f'
    else:
        formato = '.2f'

    # Ordena e filtra os Top N
    df_top = df_grouped.sort_values(by=val_col, ascending=True).tail(top_n)

    fig = px.bar(
        df_top, 
        x=val_col, 
        y=cat_col, 
        title=title,
        text_auto=formato, 
        orientation='h',
        color=val_col, 
        color_continuous_scale=color_seq 
    )

    fig.update_layout(
        xaxis_title="Valor",
        yaxis_title="Local",
        template=template,
        coloraxis_showscale=False,
        height=400 + (top_n * 25)
    )
    
    # Formatação do texto na barra
    text_fmt = '%{x:.1f}%' if is_percent else '%{x:.2f}'
    fig.update_traces(texttemplate=text_fmt, textposition="outside")

    return fig

def plot_seasonal_volume(df, time_col, title, color_seq="Reds", template="plotly_dark"):
    """
    Gera um histograma vertical mostrando o volume total de registros por período (Sazonalidade).
    """
    df_grouped = df.groupby(time_col).size().reset_index(name='Quantidade de Focos')
    
    fig = px.bar(
        df_grouped,
        x=time_col,
        y='Quantidade de Focos',
        title=title,
        color='Quantidade de Focos',
        color_continuous_scale=color_seq,
        text_auto=True
    )
    
    fig.update_layout(
        template=template,
        coloraxis_showscale=False,
        hovermode="x unified",
        xaxis=dict(
            title=dict(text="<b>Período</b>", font=dict(family="Arial Black", size=16, color="#FF4B4B"))
        ),
        yaxis=dict(
            title=dict(text="<b>Total de Focos</b>", font=dict(family="Arial Black", size=16, color="#FF4B4B"))
        )
    )
    return fig

def plot_map_density(df, lat_col, lon_col, map_style="carto-darkmatter"):
    """
    Gera um mapa de densidade (Heatmap) interativo.
    Usa a coluna 'FRP' para ponderar a intensidade, se disponível.
    """
    coluna_peso = 'FRP' if 'FRP' in df.columns else None
    
    # Ajuste de cor da legenda baseado no fundo do mapa
    legenda_cor = "white" if "dark" in map_style else "black"
    
    fig = px.density_mapbox(
        df, 
        lat=lat_col, 
        lon=lon_col,
        z=coluna_peso,
        radius=20,
        center=dict(lat=-5.0, lon=-45.0), 
        zoom=5.5,
        mapbox_style=map_style, 
        color_continuous_scale="YlOrRd",
        opacity=0.4
    )
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=500,
        coloraxis_colorbar=dict(
            title="Intensidade<br>(FRP)",
            title_font=dict(color=legenda_cor),
            tickfont=dict(color=legenda_cor),
            x=0.95, 
            len=0.8,
            bgcolor="rgba(0,0,0,0)"
        )
    )
    
    return fig

def plot_biome_distribution(df, biome_col, template="plotly_dark"):
    """
    Gera um gráfico de rosca (Donut Chart) para visualizar a distribuição proporcional por categoria.
    """
    df_grouped = df.groupby(biome_col).size().reset_index(name='Contagem')
    
    fig = px.pie(
        df_grouped, 
        names=biome_col, 
        values='Contagem', 
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    fig.update_layout(
        template=template,
        legend_title="Bioma",
        height=350
    )
    
    fig.update_traces(textinfo='percent+label')
    
    return fig