from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import pandas as pd
import numpy as np
import re 

options = Options() 
url = 'https://www.dfimoveis.com.br/'
driver = webdriver.Edge(options=options)
driver.get(url)
wait = WebDriverWait(driver, 10)

# Parametros de busca
opcao_modelo = "VENDA"
opcao_imovel = "CASA"
opcao_estado = "GO"
opcao_cidade = "APARECIDA DE GOIANIA"
opcao_bairro = "CARDOSO"
opcao_quarto = "QUARTO (TODOS)"

# Compra ou venda 
xpath = "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[1]/span/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_modelo)
element.send_keys(Keys.ENTER)

# Casa ou apartamento 
xpath = "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[2]/span/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_imovel)
element.send_keys(Keys.ENTER)

# Estado  
xpath = "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[3]/span/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_estado)
element.send_keys(Keys.ENTER)

# Cidade  
xpath = "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[4]/span/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_cidade)
element.send_keys(Keys.ENTER)

# Bairro  
xpath = "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[5]/span/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'select2-search__field')))
element.send_keys(opcao_bairro)
element.send_keys(Keys.ENTER)

# Quartos por ID
element = wait.until(EC.element_to_be_clickable((By.ID, 'select2-quartos-container')))
element.click()
opcoesQuartos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'select2-results__option')))
for opcao in opcoesQuartos:
    if opcao.text.strip() == opcao_quarto:  
        opcao.click()
        break

# Realizar busca por ID
botao_busca = wait.until(EC.element_to_be_clickable((By.ID,"botaoDeBusca")))
botao_busca.click()

lst_imoveis = []   # Lista para armazenar os imoveis
# Resultados por ID 
while True:

    xpath_resultados = '//*[@id="resultadoDaBuscaDeImoveis"]'
    resultados_container = wait.until(EC.presence_of_element_located((By.XPATH, xpath_resultados)))
    elementos = resultados_container.find_elements(By.TAG_NAME, 'a')

    for elem in elementos:
        imovel = {}
        imovel['localizacao'] = elem.find_element(By.CLASS_NAME, "new-title").text
        imovel['metragem'] = elem.find_element(By.CLASS_NAME, "new-details-ul").text
        imovel['preco'] = elem.find_element(By.CLASS_NAME, "new-price").text
        imovel['quartos'] = elem.find_element(By.CLASS_NAME, "new-details-ul").text
        imovel['decricao'] = elem.find_element(By.CLASS_NAME, "new-simple").text
        lst_imoveis.append(imovel)

    # Botao "Proxima"
    proxima_aba = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.next')))
    if proxima_aba.get_attribute("class") == "btn disabled next":
        break
    # Scroll ate o botão
    driver.execute_script("arguments[0].scrollIntoView(true);", proxima_aba)
    sleep(1)
    # Click - ignora bloqueios visuais
    driver.execute_script("arguments[0].click();", proxima_aba)
    sleep(2)

driver.quit()   # Fechar o robo 
df = pd.DataFrame(lst_imoveis)

# Tratando os dados:  
# 1. letras minusculas 
df['localizacao'] = df["localizacao"].str.lower()
df['decricao'] = df["decricao"].str.lower()

# 2. aparecer apenas a metragem ( uso de regex )
df['metragem'] = df['metragem'].str.extract(r'(\d+)[^a-zA-Z]*')   

# 2.1. aparecer apenas o preco 
df['preco'] = df['preco'].str.extract(r'R\$\s?([\d\.,]+)')    #print(df)

# 2.2 aparecer apenas o numero de quartos 
df['quartos'] = df['quartos'].str.extract(r'(\d+\s+Quartos)')

# 3. Espaços vazios viram NaN  
df.replace(r'^\s*$', np.nan, regex=True, inplace=True)  # Eliminar os espaços vazios do df

print(df.columns)
print(df)

# # Criação do banco de dados 
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
user = os.getenv('MYSQL_USER')
senha = os.getenv('MYSQL_PASSWORD')
database_name_web = os.getenv('MYSQL_DATABASE_WEB')

BASE_DIR = Path(__file__).parent
DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name_web}'
engine = create_engine(DATABASE_URL)
df.to_sql('tb_dados_imobiliarios', con=engine, if_exists='replace', index=False)    # Append: Mantém e adiciona os dados 
                                                                                    # Replace: apaga e recria os dados 
# # Criando o banco de dados no Mysql
# use db_imoveis;
# CREATE TABLE tb_dados_imobiliarios (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     localizacao VARCHAR(255),
#     metragem VARCHAR(255),
#     quartos VARCHAR(255),
#     descricao VARCHAR(255)
# ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# select * from tb_dados_imobiliarios;

 


