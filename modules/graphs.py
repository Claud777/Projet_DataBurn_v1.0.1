import plotly.express as px
import pandas as pd
import streamlit as st

def plot_line_evolution(df, x_col, y_col, title, color_hex="#FF4B4B"):
    """Gera gráfico de linha. Se x_col for mês, ordena."""
    try:
        # Agrupa
        df_grouped = df.groupby(x_col)[y_col].mean().reset_index()
    except Exception as e:
        st.error(f"Erro ao agrupar: {e}")
        return None

    fig = px.line(
        df_grouped, 
        x=x_col, 
        y=y_col, 
        title=title,
        markers=True
    )
    
    fig.update_traces(line_color=color_hex, line_width=3)
    fig.update_layout(
        xaxis_title="Período",
        yaxis_title="Média",
        hovermode="x unified",
        template="plotly_white"
    )
    
    # Se for ano (número), remove vírgula. Se for texto (mês), deixa quieto.
    if pd.api.types.is_numeric_dtype(df_grouped[x_col]):
        fig.update_xaxes(dtick=1, tickformat="d")
        
    return fig

def plot_bar_ranking(df, cat_col, val_col, title, top_n=10, color_seq="Blues", is_percent=False):
    """Gera ranking horizontal com gradiente de cor.
    Parametro is_percent: Se True, formata como porcentagem (ex: 0.5 -> 50%)"""
    # Agrupa
    df_grouped = df.groupby(cat_col)[val_col].mean().reset_index()
    
    # Se for porcentagem (Risco 0-1), multiplica por 100 para visualização
    if is_percent:
        df_grouped[val_col] = df_grouped[val_col] * 100
        formato = '.1f' # 1 casa decimal (ex: 99.5)
        sulfixo = '%'
    else:
        formato = '.2f'
        sulfixo = ''

    # Ordena e pega os top N
    df_top = df_grouped.sort_values(by=val_col, ascending=True).tail(top_n)

    fig = px.bar(
        df_top, 
        x=val_col, 
        y=cat_col, 
        title=title,
        text_auto=formato, 
        orientation='h',
        color=val_col, # Gradiente baseado no valor
        color_continuous_scale=color_seq 
    )

    fig.update_layout(
        xaxis_title="Valor",
        yaxis_title="Local",
        template="plotly_white",
        coloraxis_showscale=False,
        height=400 + (top_n * 25)
    )
    
    # Adiciona o % no texto da barra se necessário
    if is_percent:
        fig.update_traces(texttemplate='%{x:.1f}%', textposition="outside")
    else:
        fig.update_traces(textposition="outside")

    return fig