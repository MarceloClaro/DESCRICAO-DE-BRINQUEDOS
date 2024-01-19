from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Função para raspar dados com base no nome do brinquedo
def scrape_product_data(nome_brinquedo):
    # Inicialize o driver do Selenium (neste caso, o Firefox)
    driver = webdriver.Firefox()

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
        product_element = driver.find_element(By.XPATH, '/html/body/div[10]/div/div[1]/div[2]')

        # Extraia o texto do elemento para obter a descrição do produto
        descricao_produto = product_element.text

        # Encontre o elemento que contém o preço do produto (ajuste o XPath conforme necessário)
        preco_element = driver.find_element(By.XPATH, '/html/body/div[10]/div/div[1]/div[2]')

        # Extraia o texto do elemento para obter o preço do produto
        preco = preco_element.text

        # Crie um dicionário com os dados
        dados = {
            'Nome do Brinquedo': [nome_brinquedo],
            'Descrição do Produto': [descricao_produto],
            'Preço do Produto': [preco]
        }

        # Crie um DataFrame do Pandas a partir do dicionário
        df = pd.DataFrame(dados)

        # Salve os dados em um arquivo CSV com o nome do brinquedo
        csv_filename = nome_brinquedo.replace(' ', '_') + '_dados.csv'
        df.to_csv(csv_filename, index=False)

        # Imprima os resultados
        print("Nome do Brinquedo:", nome_brinquedo)
        print("Descrição do Produto:", descricao_produto)
        print("Preço do Produto:", preco)

    finally:
        # Feche o driver do Selenium, independentemente do resultado
        driver.quit()

# Pergunte ao usuário pelo nome do brinquedo
nome_brinquedo = input("Digite o nome do brinquedo a ser raspado: ")

# Chame a função de raspagem com o nome do brinquedo fornecido
scrape_product_data(nome_brinquedo)
