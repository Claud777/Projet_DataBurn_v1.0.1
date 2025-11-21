import plotly.express as px
import pandas as pd
import streamlit as st

def plot_line_evolution(df, x_col, y_col, title, color_hex="#FF4B4B"):
    """Agrupa pela coluna de tempo para evitar poluição visual."""
    # Se x_col for data, garante ordenação
    try:
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
    
    # Ux clean
    fig.update_traces(line_color=color_hex, line_width=3)
    fig.update_layout(
        xaxis_title="Período",
        yaxis_title="Média Registrada",
        hovermode="x unified", # Mostra todos os dados daquela linha vertical
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20) # Margens ajustadas
    )
    
    return fig

def plot_bar_ranking(df, cat_col, val_col, title, top_n=10):
    """Gera um gráfico de barras horizontal com o Top N locais."""
    # Agrupa e ordena para pegar os maiores
    df_grouped = df.groupby(cat_col)[val_col].mean().reset_index()
    df_top = df_grouped.sort_values(by=val_col, ascending=True).tail(top_n) # Ascending + Tail pega os maiores no topo do gráfico horizontal

    fig = px.bar(
        df_top, 
        x=val_col, 
        y=cat_col, 
        title=title,
        text_auto='.2f', # Mostra o valor na barra
        orientation='h'
    )

    fig.update_traces(marker_color="#1F77B4", textposition="outside")
    fig.update_layout(
        xaxis_title="Valor Médio",
        yaxis_title="Local",
        template="plotly_white",
        height=400 + (top_n * 10) # Ajusta altura dinamicamente
    )

    return fig