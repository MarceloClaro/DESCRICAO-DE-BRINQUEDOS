import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# Função para raspar e salvar dados em XLSX e CSV
def raspar_e_salvar_dados(url, seletor_nome, seletor_descricao, seletor_preco, nome_arquivo_base):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontre todos os elementos que correspondem ao seletor do nome do produto
    nomes = [elemento.text.strip() for elemento in soup.select(seletor_nome)]

    # Encontre todos os elementos que correspondem ao seletor da descrição
    descricoes = [elemento.text.strip() for elemento in soup.select(seletor_descricao)]

    # Encontre todos os elementos que correspondem ao seletor do preço
    precos = [elemento.text.strip() for elemento in soup.select(seletor_preco)]

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
seletor_nome = st.text_input('Insira o seletor CSS para o nome do produto:')
seletor_descricao = st.text_input('Insira o seletor CSS para a descrição:')
seletor_preco = st.text_input('Insira o seletor CSS para o preço:')
nome_arquivo_base = st.text_input('Insira o nome base dos arquivos XLSX e CSV (sem extensão):')
if st.button('Raspar e Salvar Dados'):
    raspar_e_salvar_dados(url, seletor_nome, seletor_descricao, seletor_preco, nome_arquivo_base)
