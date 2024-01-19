import streamlit as st
import requests
from bs4 import BeautifulSoup
import lxml.html
import re
import pandas as pd

def corrigir_url(url):
    url = url.strip().rstrip(',')
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def scrape_product_data(url, nome_brinquedo):
    try:
        url_corrigido = corrigir_url(url)
        response = requests.get(url_corrigido)
        soup = BeautifulSoup(response.content, 'lxml')

        # Exemplo de uso do XPath para encontrar um elemento
        tree = lxml.html.fromstring(response.content)
        xpath_descricao = 'seu_xpath_para_descricao_aqui'
        descricao_elements = tree.xpath(xpath_descricao)
        descricao_produto = descricao_elements[0].text_content().strip() if descricao_elements else 'Não encontrado'

        # Exemplo de uso de Regex para encontrar um elemento
        regex_preco = r'seu_regex_para_preco_aqui'
        preco_match = re.search(regex_preco, response.text)
        preco = preco_match.group() if preco_match else 'Não encontrado'

        return url, nome_brinquedo, descricao_produto, preco

    except Exception as e:
        st.error(f"Erro ao raspar dados para {nome_brinquedo} no site {url}: {e}")
        return url, nome_brinquedo, "Erro", "Erro"

st.title('Web Scraping de Brinquedos Avançado')

urls_input = st.text_area("Digite os URLs dos sites, separados por linha:")
urls = urls_input.split("\n")
nome_brinquedo = st.text_input("Digite o nome do brinquedo:")

if st.button('Iniciar Scraping'):
    resultados = []
    for url in urls:
        if url:
            resultado = scrape_product_data(url, nome_brinquedo)
            resultados.append(resultado)

    df_resultados = pd.DataFrame(resultados, columns=['URL', 'Nome do Brinquedo', 'Descrição do Produto', 'Preço do Produto'])
    st.write(df_resultados)
