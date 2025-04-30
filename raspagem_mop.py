from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import mysql.connector
from datetime import date
import time

print("🔎 Iniciando processo de raspagem com Selenium...")

# CONFIGURANDO SELENIUM (modo headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
servico = Service(executable_path="C:/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=servico, options=options)
# CONEXÃO COM BANCO DE DADOS
try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='CarolScott1506$',
        database='mop_mvp'
    )
    cursor = conexao.cursor()
    print("✅ Conexão com o banco de dados estabelecida!")

except mysql.connector.Error as e:
    print(f"❌ ERRO ao conectar no banco de dados: {e}")
    exit()

# PALAVRA-CHAVE DE BUSCA
palavra_chave = "Donald Trump"
urls = [
    f"https://g1.globo.com/busca/?q={palavra_chave.replace(' ', '+')}",
    f"https://busca.uol.com.br/?q={palavra_chave.replace(' ', '+')}"
]

total_salvos = 0

for url in urls:
    print(f"\n🌐 Acessando: {url}")
    try:
        driver.get(url)
        time.sleep(3)  # esperar JS carregar

        soup = BeautifulSoup(driver.page_source, "html.parser")
        resultados = []
        fonte = ""

        if "g1.globo.com" in url:
            resultados = soup.select('div.feed-post-body-title > a')
            fonte = "G1"

        elif "uol.com.br" in url:
            resultados = soup.select('div.result h2 a')
            fonte = "UOL"

        print(f"🔍 {len(resultados)} notícias encontradas no {fonte}.")

        for noticia in resultados:
            texto = noticia.text.strip()
            data_coletada = date.today()
            sentimento = "neutro"

            sql = """
            INSERT INTO tb_mencoes_coletadas 
            (tb_entidade_monitoradas_id_entidadesMonitoradas, alertas_notificacoes_id_alertas, fonte, data_coletada, texto, sentimento)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            dados = (1, None, fonte, data_coletada, texto, sentimento)
            cursor.execute(sql, dados)

            total_salvos += 1
            print(f"💾 Salvo: {texto[:60]}...")

            time.sleep(1)

    except Exception as e:
        print(f"⚠️ Erro ao processar {url}: {e}")

# FINALIZANDO
conexao.commit()
cursor.close()
conexao.close()
driver.quit()

print(f"\n✅ Raspagem concluída! Total de notícias salvas: {total_salvos}")
