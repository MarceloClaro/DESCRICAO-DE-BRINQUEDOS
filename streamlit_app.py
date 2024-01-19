import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para corrigir e completar o URL se necessário
def corrigir_url(url):
    url = url.strip().rstrip(',')  # Remove espaços e vírgulas extras
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

# Função para raspar dados com base no URL e no nome do brinquedo
def scrape_product_data(url, nome_brinquedo):
    try:
        # Corrige o URL se necessário
        url_corrigido = corrigir_url(url)

        # Faça uma requisição para o site fornecido
        response = requests.get(url_corrigido)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontre os elementos que contêm as informações do produto
        # Substitua 'seletor_css_do_produto' e 'seletor_css_do_preco' pelos seletores corretos
        product_element = soup.select_one('seletor_css_do_produto')
        descricao_produto = product_element.text.strip() if product_element else 'Não encontrado'

        preco_element = soup.select_one('seletor_css_do_preco')
        preco = preco_element.text.strip() if preco_element else 'Não encontrado'

        return url, nome_brinquedo, descricao_produto, preco

    except Exception as e:
        st.error(f"Erro ao raspar dados para {nome_brinquedo} no site {url}: {e}")
        return url, nome_brinquedo, "Erro", "Erro"

# Inicialização do Streamlit
st.title('Web Scraping de Brinquedos')

# Input do usuário para URLs e nome do brinquedo
urls_input = st.text_area("Digite os URLs dos sites, separados por linha:")
urls = urls_input.split("\n")

nome_brinquedo = st.text_input("Digite o nome do brinquedo:")

if st.button('Iniciar Scraping'):
    # Lista para armazenar os resultados
    resultados = []

    for url in urls:
        if url:  # Verifica se a URL não está vazia
            resultado = scrape_product_data(url, nome_brinquedo)
            resultados.append(resultado)

    # Convertendo os resultados para DataFrame
    df_resultados = pd.DataFrame(resultados, columns=['URL', 'Nome do Brinquedo', 'Descrição do Produto', 'Preço do Produto'])
    
    # Mostrando os resultados no Streamlit
    st.write(df_resultados)
