# Projet_DataBurn_v1.0.1

## Análise de Big Data e Dashboard Streamlit

Este projeto tem como objetivo realizar uma análise aprofundada de dados reais (Big Data) para identificar a causa raiz de um problema de negócio específico. O projeto utiliza Python para processamento de dados e o Streamlit para a criação de um dashboard interativo, permitindo que o time de front-end desenvolva o design e que os resultados da análise sejam visualizados de forma clara.

## Estrutura do Projeto

A estrutura de diretórios e arquivos é organizada da seguinte forma:

```
Projet_DataBurn_v1.0.1/
├── data/
│   ├── db_2020/
│   │   └── dados_2020.csv
│   ├── db_2021/
│   │   └── dados_2021.csv
│   ├── ...
│   └── db_2025/
│       └── db_2025.csv
├── results/
│   └── estatisticas.txt  # Resultados da análise estatística
├── scripts/
│   ├── csv_analyzer.py   # Scripts de análise de dados
│   └── csv_analyzer2.py
├── app.py                # Aplicação principal do dashboard Streamlit
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

## Como Rodar o Dashboard Streamlit

Para executar o dashboard localmente, siga os passos abaixo:

### 1. Pré-requisitos

Certifique-se de ter o **Python 3** instalado no seu sistema.

### 2. Clonar o Repositório

Se você ainda não o fez, clone o repositório e acesse o diretório do projeto:

```bash
git clone https://github.com/Claud777/Projet_DataBurn_v1.0.1.git
cd Projet_DataBurn_v1.0.1
```

### 3. Instalar as Dependências

É altamente recomendável usar um ambiente virtual (`venv`) para isolar as dependências do projeto.

```bash
# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows

# Instale as dependências listadas no requirements.txt
pip install -r requirements.txt
```

### 4. Executar a Aplicação

Com o ambiente ativado e as dependências instaladas, execute o Streamlit:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

---
*Este README foi gerado automaticamente para documentação inicial do projeto.*
