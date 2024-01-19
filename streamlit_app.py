import streamlit as st
from requests_html import HTMLSession
import pandas as pd

def corrigir_url(url):
    url = url.strip().rstrip(',')
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def scrape_product_data(url, nome_brinquedo):
    try:
        url_corrigido = corrigir_url(url)
        session = HTMLSession()
        response = session.get(url_corrigido)

        # Renderiza a página, incluindo JavaScript
        response.html.render()

        # Substitua os seletores abaixo com os seletores CSS adequados
        descricao_produto = response.html.find('seletor_css_para_descricao', first=True).text
        preco = response.html.find('seletor_css_para_preco', first=True).text

        return url, nome_brinquedo, descricao_produto, preco

    except Exception as e:
        st.error(f"Erro ao raspar dados para {nome_brinquedo} no site {url}: {e}")
        return url, nome_brinquedo, "Erro", "Erro"

st.title('Web Scraping de Brinquedos com Requests-HTML')

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
