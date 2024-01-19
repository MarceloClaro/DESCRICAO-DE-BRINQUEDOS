import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para raspar dados com base no nome do brinquedo
def scrape_product_data(nome_brinquedo):
    try:
        # Faça uma requisição para o site de comércio eletrônico
        url = f'https://plantandoebrincando.com.br/search?q={nome_brinquedo}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontre os elementos que contêm as informações do produto
        # Substitua 'seletor_css_do_produto' pelo seletor CSS correto
        product_element = soup.select_one('seletor_css_do_produto')
        descricao_produto = product_element.text.strip() if product_element else 'Não encontrado'

        # Substitua 'seletor_css_do_preco' pelo seletor CSS correto
        preco_element = soup.select_one('seletor_css_do_preco')
        preco = preco_element.text.strip() if preco_element else 'Não encontrado'

        return nome_brinquedo, descricao_produto, preco

    except Exception as e:
        st.error(f"Erro ao raspar dados para {nome_brinquedo}: {e}")
        return nome_brinquedo, "Erro", "Erro"

# Inicialização do Streamlit
st.title('Web Scraping de Brinquedos')

# Input do usuário
nomes_brinquedos = st.text_area("Digite os nomes dos brinquedos, separados por linha:")
lista_brinquedos = nomes_brinquedos.split("\n")

if st.button('Iniciar Scraping'):
    # Lista para armazenar os resultados
    resultados = []

    for nome in lista_brinquedos:
        if nome:  # Verifica se o nome não está vazio
            resultado = scrape_product_data(nome)
            resultados.append(resultado)

    # Convertendo os resultados para DataFrame
    df_resultados = pd.DataFrame(resultados, columns=['Nome do Brinquedo', 'Descrição do Produto', 'Preço do Produto'])
    
    # Mostrando os resultados no Streamlit
    st.write(df_resultados)
