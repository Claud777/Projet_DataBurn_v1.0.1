import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_multiple_years(years):
    """Carrega e concatena os dados de múltiplos anos."""
    all_data = []
    errors = []
    
    # Garante que years é uma lista, mesmo que venha um só
    if not isinstance(years, list):
        years = [years]

    for year in years:
        path = f"data/db_{year}/dados_{year}.csv"
        if os.path.exists(path):
            try:
                df_temp = pd.read_csv(path)
                df_temp['ano_origem'] = year 
                all_data.append(df_temp)
            except Exception as e:
                errors.append(f"Erro ao ler {year}: {e}")
        else:
            errors.append(f"Arquivo não encontrado para {year}")
    
    if errors:
        for err in errors:
            st.warning(err)
            
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return None