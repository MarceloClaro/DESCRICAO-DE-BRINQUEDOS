import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def corrigir_url(url):
    url = url.strip().rstrip(',')
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def scrape_product_data(url, nome_brinquedo):
    try:
        url_corrigido = corrigir_url(url)

        # Configuração para rodar o navegador em modo headless
        options = Options()
        options.headless = True

        # Configuração do driver usando webdriver_manager para Chrome
        with webdriver.Chrome(ChromeDriverManager().install(), options=options) as driver:
            driver.get(url_corrigido)
            time.sleep(5)  # Espera para o JavaScript carregar

            # Realize o scraping aqui
            # Você precisará ajustar o código abaixo para se adaptar ao seu caso específico
            # Exemplo: encontrar um elemento pelo XPath e extrair o texto
            elemento = driver.find_element_by_xpath('seu_xpath_aqui')
            descricao_produto = elemento.text if elemento else 'Não encontrado'

            # Exemplo para preço do produto
            elemento_preco = driver.find_element_by_xpath('seu_xpath_para_preco_aqui')
            preco = elemento_preco.text if elemento_preco else 'Não encontrado'

            return url, nome_brinquedo, descricao_produto, preco

    except Exception as e:
        st.error(f"Erro ao raspar dados para {nome_brinquedo} no site {url}: {e}")
        return url, nome_brinquedo, "Erro", "Erro"

st.title('Web Scraping de Brinquedos com Selenium e Chrome Headless')

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
