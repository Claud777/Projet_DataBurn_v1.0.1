import pandas as pd

""" Funções utilitárias para o projeto"""

def formatar_numero(valor, decimais=0):
    """Formata número para padrão brasileiro."""
    if pd.isna(valor): return "0,00"
    s = f"{valor:,.{decimais}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")