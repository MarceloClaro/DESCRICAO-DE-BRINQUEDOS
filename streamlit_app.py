import requests
from bs4 import BeautifulSoup
import json
import streamlit as st

# Função auxiliar para raspar sublinks
def raspar_sublinks(url, seletores):
    try:
        response = requests.get(url)
        sub_soup = BeautifulSoup(response.text, 'html.parser')
        sub_dados = {}
        for seletor in seletores:
            sub_elementos = sub_soup.find_all(seletor)
            sub_dados[seletor] = [elemento.get_text().strip() for elemento in sub_elementos]
        return sub_dados
    except requests.RequestException:
        return None

# Função para raspar e salvar JSON
def raspar_e_salvar_json(url, seletores, nome_arquivo_json):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    dados = {seletor: [elemento.get_text().strip() for elemento in soup.find_all(seletor)] for seletor in seletores}

    # Raspagem de sublinks
    sublinks = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
    dados_sublinks = {sublink: raspar_sublinks(sublink, seletores) for sublink in sublinks}

    # Raspagem de sub-sublinks
    for sublink, sub_dados in dados_sublinks.items():
        if sub_dados:
            sub_sublinks = [a['href'] for a in BeautifulSoup(requests.get(sublink).text, 'html.parser').find_all('a', href=True) if a['href'].startswith('http')]
            sub_dados['sub_sublinks'] = {sub_sublink: raspar_sublinks(sub_sublink, seletores) for sub_sublink in sub_sublinks}

    dados['sublinks'] = dados_sublinks

    # Salvar os dados em JSON
    with open(nome_arquivo_json, 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)

# Configurar a interface do Streamlit
st.title('Raspagem de Dados HTML com Streamlit')
url = st.text_input('Insira a URL que deseja raspar:')
seletores = st.text_input('Insira os seletores HTML que deseja usar (separados por vírgula):')
nome_arquivo_json = st.text_input('Insira o nome do arquivo JSON para salvar os dados:')
if st.button('Raspar e Salvar JSON'):
    # Converter a string de seletores em uma lista
    seletores = [s.strip() for s in seletores.split(',')]
    # Executar a função de raspagem com os valores fornecidos pelo usuário
    raspar_e_salvar_json(url, seletores, nome_arquivo_json)
    st.success(f'Dados raspados e salvos em {nome_arquivo_json}')
