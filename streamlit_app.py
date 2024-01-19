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
            # O primeiro seletor é para o nome do produto
            nomes = [elemento.text.strip() for elemento in elementos]
        elif seletor == seletores[1]:
            # O segundo seletor é para a descrição
            descricoes = [elemento.text.strip() for elemento in elementos]
        elif seletor == seletores[2]:
            # O terceiro seletor é para o preço
            precos = [elemento.text.strip() for elemento in elementos]

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
    # Converter a string de seletores em uma lista
    seletores = [s.strip() for s in seletores.split(',')]
    # Executar a função de raspagem com os valores fornecidos pelo usuário
    arquivo_xlsx, arquivo_csv = raspar_e_salvar_dados(url, seletores, nome_arquivo_base)
    st.success(f'Dados raspados e salvos em {arquivo_xlsx} e {arquivo_csv}')
