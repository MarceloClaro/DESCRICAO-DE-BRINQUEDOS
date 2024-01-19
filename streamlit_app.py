import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configuração do Streamlit
st.title('Raspagem de Dados de Produtos')

# Interface do usuário para inserir o nome do produto
product_name = st.text_input('Digite o nome do produto a ser pesquisado:')
if st.button('Pesquisar e Raspagem de Dados'):
    # Inicializar o driver do Selenium
    driver = webdriver.Chrome(executable_path='seu_caminho_para_o_chromedriver')

    # Função para pesquisar e raspar dados
    def search_and_scrape(product_name):
        # Navegar para a página de pesquisa
        driver.get('https://exemplo.com/pagina_de_pesquisa')

        # Localizar a barra de pesquisa e inserir o nome do produto
        search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_box.send_keys(product_name)

        # Submeter o formulário de pesquisa (ajuste o seletor conforme necessário)
        search_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

        # Aguarde até que a página de resultados seja carregada (ajuste o tempo limite conforme necessário)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html body.js-head-offset.head-offset.transition-long.template-search section.category-body div.container div.js-product-table.row a.js-item-link.item-link.position-absolute.w-100')))

        # Localize todos os links dos produtos após a pesquisa
        product_links = driver.find_elements(By.CSS_SELECTOR, 'html body.js-head-offset.head-offset.transition-long.template-search section.category-body div.container div.js-product-table.row a.js-item-link.item-link.position-absolute.w-100')

        # Inicialize listas para armazenar dados
        product_names = []
        product_prices = []
        product_descriptions = []
        image_urls = []

        # Extraia os links e avance para cada página
        for link in product_links:
            product_link = link.get_attribute("href")

            # Abra o link do produto
            driver.get(product_link)

            # Aguarde até que a próxima página seja carregada (ajuste o tempo limite conforme necessário)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-title h1')))

            # Coletar informações do produto
            product_name = driver.find_element(By.CSS_SELECTOR, '.product-title h1').text
            product_price = driver.find_element(By.CSS_SELECTOR, 'span.d-inline-block h4#price_display.js-price-display.h2.mb-2.text-brand').text
            product_description = driver.find_element(By.CSS_SELECTOR, '.product-description').text

            # Coletar a URL da imagem
            image_element = driver.find_element(By.CSS_SELECTOR, 'div.js-product-slide:nth-child(1) > a:nth-child(1) > img:nth-child(1)')
            image_url = image_element.get_attribute("src")

            # Adicionar informações às listas
            product_names.append(product_name)
            product_prices.append(product_price)
            product_descriptions.append(product_description)
            image_urls.append(image_url)

            # Retornar à página de resultados de pesquisa
            driver.back()

            # Aguarde até que a página de resultados de pesquisa seja carregada novamente
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="search"]')))

        # Criar um DataFrame do Pandas com os dados coletados
        data = {
            'Nome do Produto': product_names,
            'Preço do Produto': product_prices,
            'Descrição do Produto': product_descriptions,
            'URL da Imagem': image_urls
        }
        df = pd.DataFrame(data)

        # Salvar os dados em um arquivo CSV
        df.to_csv('dados_produtos.csv', index=False)

        # Finalizar o driver
        driver.quit()

    # Chame a função para pesquisar e raspar dados
    search_and_scrape(product_name)
