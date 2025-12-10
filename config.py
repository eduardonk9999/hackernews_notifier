from dotenv import load_dotenv
import os

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # lê token
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")      # lê id do chat