from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import mysql.connector
import time
import traceback

# ========== CONFIGURAÇÃO INICIAL ==========
palavra_chave = "Donald Trump "
palavra_chave_formatada = palavra_chave.replace(' ', '+')

entidade_id = 1
alerta_id = 1
fonte_g1 = 'G1'
fonte_google = 'Google Notícias'
data_coletada = datetime.today().strftime('%Y-%m-%d')
sentimento = 'neutro'

# ========== RASPAGEM G1 COM SELENIUM ==========
def raspar_g1(palavra_chave):
    print("📺 Iniciando raspagem do G1...")
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    servico = Service(executable_path="C:/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=servico, options=options)

    palavra_chave_formatada = palavra_chave.replace(' ', '+')
    url_g1 = f"https://g1.globo.com/busca/?q={palavra_chave_formatada}"
    print(f"🌐 Acessando: {url_g1}")
    resultados = []

    try:
        driver.get(url_g1)
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.widget--info__title.product-color'))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        titulos = soup.select('div.widget--info__title.product-color')

        print(f"✅ {len(titulos)} títulos encontrados no G1.")

        for noticia in titulos:
            titulo = noticia.get_text().strip()
            a_tag = noticia.find_parent('a')
            link = a_tag['href'] if a_tag else None
            resultados.append((titulo, link))

    except Exception as e:
        print(f"⚠️ Erro ao raspar G1: {e}")
        traceback.print_exc()
    finally:
        driver.quit()

    return resultados

# ========== RASPAGEM GOOGLE NOTÍCIAS COM REQUESTS ==========
def raspar_google_news(palavra_chave):
    print("🔎 Iniciando raspagem do Google Notícias (via requests)...")
    resultados = []
    palavra_chave_formatada = palavra_chave.replace(' ', '+')
    url = f"https://www.google.com/search?q={palavra_chave_formatada}&tbm=nws"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
    }

    try:
        print(f"🌐 Acessando: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        blocos_noticias = soup.select("a[href^='https://']")

        for bloco in blocos_noticias:
            texto = bloco.get_text().strip()
            link = bloco['href']
            if texto and len(texto.split()) > 3:
                resultados.append((texto, link))

        print(f"✅ {len(resultados)} títulos encontrados no Google Notícias.")

    except Exception as e:
        print(f"⚠️ Erro ao raspar Google Notícias: {e}")
        traceback.print_exc()

    return resultados

# ========== INSERÇÃO NO BANCO ==========
def inserir_no_banco(titulos_com_links, fonte):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='CarolScott1506$',
        database='mop_mvp'
    )
    cursor = conexao.cursor()
    for titulo, link in titulos_com_links:
        print(f"💾 Inserindo: {titulo} [{fonte}] - Link: {link}")
        cursor.execute("""
            INSERT INTO tb_mencoes_coletadas (
                tb_entidade_monitoradas_id_entidadesMonitoradas,
                alertas_notificacoes_id_alertas,
                fonte,
                data_coletada,
                texto,
                link,
                sentimento
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (entidade_id, alerta_id, fonte, data_coletada, titulo, link, sentimento))
    conexao.commit()
    cursor.close()
    conexao.close()

# ========== EXECUÇÃO DIRETA ==========
if __name__ == "__main__":
    print("🔎 Iniciando processo de raspagem...")
    titulos_g1 = raspar_g1(palavra_chave)
    inserir_no_banco(titulos_g1, fonte_g1)

    titulos_google = raspar_google_news(palavra_chave)
    inserir_no_banco(titulos_google, fonte_google)

    print("✅ Raspagem e inserção concluídas com sucesso!")