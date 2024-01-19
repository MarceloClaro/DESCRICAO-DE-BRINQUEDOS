import requests
from bs4 import BeautifulSoup
import json
import streamlit as st

# Função para raspar e salvar JSON
def raspar_e_salvar_json(url, seletores, nome_arquivo_json):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Inicialize um dicionário vazio para armazenar os dados
    dados = {'produtos': []}

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

    # Combinar as listas de nomes, descrições e preços em um único dicionário
    for nome, descricao, preco in zip(nomes, descricoes, precos):
        produto = {
            'Nome do Produto': nome,
            'Descrição': descricao,
            'Preço': preco
        }
        dados['produtos'].append(produto)

    # Salvar os dados em JSON
    with open(nome_arquivo_json, 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)

# Configurar a interface do Streamlit
st.title('Raspagem de Dados HTML com Streamlit')
url = st.text_input('Insira a URL que deseja raspar:')
seletores = st.text_input('Insira os seletores HTML para o nome do produto, descrição e preço (separados por vírgula):')
nome_arquivo_json = st.text_input('Insira o nome do arquivo JSON para salvar os dados:')
if st.button('Raspar e Salvar JSON'):
    # Converter a string de seletores em uma lista
    seletores = [s.strip() for s in seletores.split(',')]
    # Executar a função de raspagem com os valores fornecidos pelo usuário
    raspar_e_salvar_json(url, seletores, nome_arquivo_json)
    st.success(f'Dados raspados e salvos em {nome_arquivo_json}')
