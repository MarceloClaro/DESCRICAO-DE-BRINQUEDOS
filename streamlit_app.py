import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

def initialize_webdriver():
    options = Options()
    options.headless = True  # Configuração para modo headless
    # Configuração do driver usando webdriver_manager
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    return driver

# Em seguida, use esta função para inicializar o Selenium WebDriver em seu script
driver = initialize_webdriver()
# Seu código de scraping aqui...

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
        with webdriver.Firefox(options=options) as driver:
            driver.get(url_corrigido)
            
            # Aguarde o JavaScript carregar (ajuste o tempo conforme necessário)
            time.sleep(5)  # Espera 5 segundos

            # Realize o scraping aqui
            # Exemplo: encontrar um elemento pelo XPath e extrair o texto
            # Substitua 'seu_xpath_aqui' pelo XPath correto
            elemento = driver.find_element_by_xpath('seu_xpath_aqui')
            descricao_produto = elemento.text if elemento else 'Não encontrado'

            # Substitua 'seu_xpath_para_preco_aqui' pelo XPath correto
            elemento_preco = driver.find_element_by_xpath('seu_xpath_para_preco_aqui')
            preco = elemento_preco.text if elemento_preco else 'Não encontrado'

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
