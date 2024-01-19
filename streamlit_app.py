import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configuração do Streamlit
st.title('Raspagem de Dados de Produtos')

# Interface do usuário para inserir a URL da página de pesquisa e o nome do produto
url = st.text_input('Insira a URL da página de pesquisa:')
product_name = st.text_input('Digite o nome do produto que deseja buscar:')

if st.button('Pesquisar e Raspagem de Dados'):
    try:
        # Enviar uma solicitação HTTP para a URL
        response = requests.get(url)
        response.raise_for_status()

        # Analisar o conteúdo da página com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Localize os elementos HTML com base na estrutura da página e no nome do produto
        product_names = [element.text.strip() for element in soup.select('.product-title h1') if product_name in element.text]
        product_prices = [element.text.strip() for element in soup.select('span.d-inline-block h4#price_display.js-price-display.h2.mb-2.text-brand') if product_name in element.text]
        product_descriptions = [element.text.strip() for element in soup.select('.product-description') if product_name in element.text]
        image_urls = [element.get('src') for element in soup.select('div.js-product-slide:nth-child(1) > a:nth-child(1) > img:nth-child(1)') if product_name in element.get('alt')]

        # Criar um DataFrame do Pandas com os dados coletados
        data = {
            'Nome do Produto': product_names,
            'Preço do Produto': product_prices,
            'Descrição do Produto': product_descriptions,
            'URL da Imagem': image_urls
        }
        df = pd.DataFrame(data)

        # Exibir a tabela no Streamlit
        st.write(df)

        # Salvar os dados em um arquivo CSV (opcional)
        # df.to_csv('dados_produtos.csv', index=False)

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a URL: {str(e)}")
    except Exception as e:
        st.error(f"Erro durante a raspagem: {str(e)}")
