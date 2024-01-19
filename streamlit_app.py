import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Função para raspar dados com base no nome do brinquedo
def scrape_product_data(nome_brinquedo, driver):
    try:
        # Abra a URL do site de comércio eletrônico
        driver.get('https://plantandoebrincando.com.br')

        # Encontre o campo de pesquisa e insira o nome do brinquedo
        search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_box.send_keys(nome_brinquedo)
        search_box.submit()

        # Aguarde até que os resultados da pesquisa sejam carregados (ajuste o tempo limite conforme necessário)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'resultado-da-pesquisa')))

        # Agora, encontre o elemento que contém as informações do produto (ajuste o XPath conforme necessário)
        product_element = driver.find_element(By.XPATH, 'xpath_do_produto')
        descricao_produto = product_element.text

        # Encontre o elemento que contém o preço do produto (ajuste o XPath conforme necessário)
        preco_element = driver.find_element(By.XPATH, 'xpath_do_preco')
        preco = preco_element.text

        return nome_brinquedo, descricao_produto, preco

    except Exception as e:
        print(f"Erro ao raspar dados para {nome_brinquedo}: {e}")
        return nome_brinquedo, "Erro", "Erro"

# Inicialização do Streamlit
st.title('Web Scraping de Brinquedos')

# Input do usuário
nomes_brinquedos = st.text_area("Digite os nomes dos brinquedos, separados por linha:")
lista_brinquedos = nomes_brinquedos.split("\n")

if st.button('Iniciar Scraping'):
    # Inicialize o driver do Selenium
    driver = webdriver.Firefox()
    
    # Lista para armazenar os resultados
    resultados = []

    for nome in lista_brinquedos:
        if nome:  # Verifica se o nome não está vazio
            resultado = scrape_product_data(nome, driver)
            resultados.append(resultado)

    driver.quit()

    # Convertendo os resultados para DataFrame
    df_resultados = pd.DataFrame(resultados, columns=['Nome do Brinquedo', 'Descrição do Produto', 'Preço do Produto'])
    
    # Mostrando os resultados no Streamlit
    st.write(df_resultados)

# Executar o app: streamlit run seu_script.py
