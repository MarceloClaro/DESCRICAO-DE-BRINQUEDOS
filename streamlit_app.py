import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para realizar a raspagem com base no nome do produto
def raspar_com_base_no_nome(url, nome_produto):
    try:
        # Enviar uma solicitação HTTP para a URL
        response = requests.get(url)
        response.raise_for_status()

        # Analisar o conteúdo da página com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Localizar os elementos HTML com base na estrutura da página
        product_names = [element.text.strip() for element in soup.select('.product-title h1') if nome_produto.lower() in element.text.lower()]
        product_prices = [element.text.strip() for element in soup.select('span.d-inline-block h4#price_display.js-price-display.h2.mb-2.text-brand') if nome_produto.lower() in element.text.lower()]
        product_descriptions = [element.text.strip() for element in soup.select('.product-description') if nome_produto.lower() in element.text.lower()]
        image_urls = [element.get('src') for element in soup.select('div.js-product-slide:nth-child(1) > a:nth-child(1) > img:nth-child(1)') if nome_produto.lower() in element.get('alt').lower()]

        # Verificar se há dados encontrados
        if not product_names:
            st.warning(f'Nenhum produto com o nome "{nome_produto}" encontrado na página.')
        else:
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

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a URL: {str(e)}")
    except Exception as e:
        st.error(f"Erro durante a raspagem: {str(e)}")

# Configuração do Streamlit
st.title('Raspagem de Dados de Produtos por Nome')
url = st.text_input('Insira a URL da página de pesquisa:')
nome_produto = st.text_input('Insira o Nome do Produto para busca:')
if st.button('Pesquisar e Raspagem de Dados'):
    raspar_com_base_no_nome(url, nome_produto)
