import requests
from bs4 import BeautifulSoup
import json
import streamlit as st
import pandas as pd

# Função para raspar e salvar dados em XLSX e CSV
def raspar_e_salvar_dados(url, seletores, nome_arquivo_base):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Inicialize listas para armazenar os dados
    nomes = []
    descricoes = []
    precos = []

    # Iterar sobre os seletores fornecidos pelo usuário
    for seletor in seletores:
        elementos = soup.select(seletor)
        if seletor == seletores[0]:
            nomes = [elemento.text.strip() for elemento in elementos]
        elif seletor == seletores[1]:
            descricoes = [elemento.text.strip() for elemento in elementos]
        elif seletor == seletores[2]:
            precos = [elemento.text.strip() for elemento in elementos]

    # Verificar se os arrays têm o mesmo comprimento
    if len(nomes) != len(descricoes) or len(nomes) != len(precos):
        st.error("Os seletores não retornaram arrays de mesmo comprimento. Verifique os seletores fornecidos.")
        return

    # Criar um DataFrame com os dados
    dados = pd.DataFrame({
        'Nome do Produto': nomes,
        'Descrição': descricoes,
        'Preço': precos
    })

    # Salvar os dados em XLSX
    arquivo_xlsx = f'{nome_arquivo_base}.xlsx'
    dados.to_excel(arquivo_xlsx, index=False)

    # Salvar os dados em CSV
    arquivo_csv = f'{nome_arquivo_base}.csv'
    dados.to_csv(arquivo_csv, index=False)

    # Apresentar a tabela no Streamlit
    st.write(dados)

    # Retornar os nomes dos arquivos salvos
    return arquivo_xlsx, arquivo_csv

# Configurar a interface do Streamlit
st.title('Raspagem de Dados HTML com Streamlit')
url = st.text_input('Insira a URL que deseja raspar:')
seletores = st.text_input('Insira os seletores HTML para o nome do produto, descrição e preço (separados por vírgula):')
nome_arquivo_base = st.text_input('Insira o nome base dos arquivos XLSX e CSV (sem extensão):')
if st.button('Raspar e Salvar Dados'):
    seletores = [s.strip() for s in seletores.split(',')]
    raspar_e_salvar_dados(url, seletores, nome_arquivo_base)
