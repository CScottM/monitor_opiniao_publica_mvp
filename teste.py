from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import traceback

print("🔎 Iniciando processo de raspagem com Selenium...")

# CONFIGURANDO SELENIUM (modo gráfico)
options = Options()
# options.add_argument("--headless")  # Remova o comentário para rodar em modo invisível
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Defina o caminho do seu chromedriver
servico = Service(executable_path="C:/chromedriver/chromedriver.exe")  # ajuste conforme seu sistema
driver = webdriver.Chrome(service=servico, options=options)

# PALAVRA-CHAVE DE BUSCA
palavra_chave = "Donald Trump"
palavra_chave_formatada = palavra_chave.replace(' ', '+')

# URL de busca no G1
url_g1 = f"https://g1.globo.com/busca/?q={palavra_chave_formatada}"
print(f"🌐 Acessando: {url_g1}")

try:
    driver.get(url_g1)

    # Aguarda até que os elementos dos títulos estejam presentes
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.widget--info__title.product-color'))
    )

    print("🔍 Página carregada. Verificando conteúdo...")

    # Obtém o HTML carregado da página
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Seleciona os títulos das notícias
    resultados = soup.select('div.widget--info__title.product-color')
    print(f"🔍 {len(resultados)} títulos encontrados no G1.")

    # Exibe os títulos coletados
    for noticia in resultados:
        titulo = noticia.get_text().strip()
        print(f"💾 Título: {titulo}")

except Exception as e:
    print(f"⚠️ Erro ao processar a URL: {e}")
    traceback.print_exc()

# Finaliza o navegador
driver.quit()
print("✅ Raspagem concluída!")
