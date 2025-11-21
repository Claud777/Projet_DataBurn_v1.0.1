# modules/data_loader.py
import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_multiple_years(years):
    """Carrega e concatena dados de múltiplos anos.
    Tenta vários padrões de caminho para encontrar o arquivo."""
    all_data = []
    errors = []
    
    # Garante que years é uma lista
    if not isinstance(years, list):
        years = [years]

    for year in years:
        
        possible_paths = [
            f"data/db_{year}/dados_{year}.csv", # Padrão original
            f"dados_{year}.csv" # Apenas o nome
        ]
        
        file_found = False
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    df_temp = pd.read_csv(path, sep=',') 
                    
                    # Normaliza nomes de colunas (remove espaços extras)
                    df_temp.columns = df_temp.columns.str.strip()
                    
                    df_temp['ano_origem'] = year 
                    all_data.append(df_temp)
                    file_found = True
                    break
                except Exception as e:
                    errors.append(f"Erro ao ler {path}: {e}")
        
        if not file_found:
            errors.append(f"Arquivo para o ano {year} não encontrado.")
            pass
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return None