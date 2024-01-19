import streamlit as st
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

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

        # Encontrar todos os textos na página
        all_text = soup.get_text()

        # Usar regex para encontrar informações com base no nome do produto
        pattern = re.compile(f'.*{re.escape(product_name)}.*', re.IGNORECASE)
        matches = pattern.findall(all_text)

        # Criar listas para armazenar informações encontradas
        product_names = []
        product_prices = []
        product_descriptions = []

        # Extrair informações com base nos padrões encontrados
        for match in matches:
            # Verificar se a correspondência contém informações de produto (ajuste conforme necessário)
            if re.search(r'Preço:', match) and re.search(r'Descrição:', match):
                product_names.append(re.search(r'(.*?)(Preço:|Descrição:)', match).group(1).strip())
                product_prices.append(re.search(r'Preço:(.*?)(Descrição:|$)', match).group(1).strip())
                product_descriptions.append(re.search(r'Descrição:(.*?)(Preço:|$)', match).group(1).strip())

        # Criar um DataFrame do Pandas com os dados coletados
        data = {
            'Nome do Produto': product_names,
            'Preço do Produto': product_prices,
            'Descrição do Produto': product_descriptions
        }
        df = pd.DataFrame(data)

        # Exibir a tabela no Streamlit
        st.write(df)

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a URL: {str(e)}")
    except Exception as e:
        st.error(f"Erro durante a raspagem: {str(e)}")
