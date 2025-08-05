from flask import Flask, render_template, request
import raspagem_mop
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    erro = None

    if request.method == 'POST':
        palavra_chave = request.form['palavra_chave']
        try:
            resultados_g1 = raspagem_mop.raspar_g1(palavra_chave)
            resultados_google = raspagem_mop.raspar_google_news(palavra_chave)
            # Adapte para o formato esperado pelo template
            data_coletada = datetime.today().strftime('%Y-%m-%d')
            sentimento = 'neutro'
            resultados = [
                (texto, link, data_coletada, sentimento)
                for (texto, link) in (resultados_g1 + resultados_google)
            ]
            print("Resultados da busca:", resultados)  # Debug
        except Exception as e:
            erro = f"Ocorreu um erro ao buscar: {str(e)}"
    else:
        # BUSCA NO BANCO DE DADOS PARA MOSTRAR O HISTÓRICO
        try:
            conexao = raspagem_mop.mysql.connector.connect(
                host='localhost',
                user='root',
                password='CarolScott1506$',
                database='mop_mvp'
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT texto, link, data_coletada, sentimento FROM tb_mencoes_coletadas ORDER BY id_mencoesColetadas DESC LIMIT 50")
            resultados = cursor.fetchall()
            cursor.close()
            conexao.close()
        except Exception as e:
            erro = f"Erro ao buscar histórico no banco: {str(e)}"

    return render_template('index.html', resultados=resultados, erro=erro)

if __name__ == "__main__":
    app.run(debug=True)