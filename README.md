# 🧠 Monitor de Opinião Pública (MOP)

O **Monitor de Opinião Pública (MOP)** é uma aplicação voltada à **coleta, organização e análise de menções públicas** sobre pessoas e instituições em sites de notícias e redes sociais. Seu objetivo é fornecer **indicadores reputacionais** e apoiar processos de tomada de decisão baseados em dados.

## 🚀 Objetivos do Projeto

- Rastrear menções públicas sobre nomes e instituições em portais de notícias.
- Realizar **análise de sentimento** com base nos textos coletados.
- Armazenar os dados em um banco relacional.
- Fornecer visualizações básicas para interpretação das informações.

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **BeautifulSoup** e **Requests** – raspagem de dados
- **MySQL / MariaDB** – banco de dados
- **Flask** – servidor e interface CRUD (em desenvolvimento)
- **NLTK** / **TextBlob** – análise de sentimentos (planejado)
- **HTML + CSS** – visualização de dados (em desenvolvimento)

## 📁 Estrutura do Projeto

```
monitor_opiniao_publica_mvp/
├── raspagem_mop.py         # Script de raspagem de dados
├── config.py               # Configurações do banco de dados
├── templates/              # HTML para interface web
├── static/                 # CSS e JS
├── database/               # Scripts SQL e backups
├── app.py                  # Servidor Flask (em desenvolvimento)
└── README.md               # Este documento
```

## 🔄 Como Usar

1. **Clone este repositório:**

```bash
git clone https://github.com/SEU_USUARIO/monitor_opiniao_publica_mvp.git
cd monitor_opiniao_publica_mvp
```

2. **Crie um ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure o acesso ao banco de dados:**

Edite o arquivo `config.py` com suas credenciais MySQL:

```python
db_config = {
    'host': 'localhost',
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'database': 'mop_mvp'
}
```

5. **Rode o script de raspagem:**

```bash
python raspagem_mop.py
```

## 🧪 Status do Projeto

🚧 **Em desenvolvimento.**  
Atualmente finalizando a versão MVP com coleta e armazenamento de dados. A próxima sprint incluirá:

- Interface CRUD para gerenciar os dados
- Relatórios de sentimento
- Dashboard com visualizações

## 👩‍💻 Idealização e Desenvolvimento

**Carolina de Souza Scott**  
Especialista em comunicação, análise de dados e estratégias digitais.  
Em transição de carreira para tecnologia, com foco em aplicações de dados e reputação pública.
