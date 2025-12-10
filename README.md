# HackerNews Notifier

Um script em Python que obtém automaticamente as 10 principais notícias do site [The Hacker News](https://thehackernews.com/) no final do dia e envia para o Telegram.

---

## 🚀 Funcionalidades

- Web scraping das manchetes da página inicial
- Seleciona as **10 notícias principais**
- Envia formatação bonitinha para o Telegram
- Pode ser agendado para rodar diariamente
- Código simples e bem organizado

---

## 🧩 Estrutura do projeto

hackernews_notifier/
│── bot.py # script principal
│── scraper.py # coleta das notícias
│── telegram_sender.py # envio para Telegram
│── config.py # tokens e configurações
│── requirements.txt # dependências
│── README.md # este arquivo
│── .env # credenciais privadas


---

## ⚙️ Instalação

Crie um ambiente virtual (opcional, recomendado):

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt


Crie um arquivo .env na raiz do projeto:
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
