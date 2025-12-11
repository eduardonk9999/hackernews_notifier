"""
Script auxiliar para obter o Chat ID do Telegram.
Envie uma mensagem para o bot primeiro, depois execute este script.
"""

import requests
import sys
from config import TELEGRAM_BOT_TOKEN

# Configura encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def obter_chat_id():
    """
    Obtém o Chat ID do Telegram fazendo uma requisição à API.
    """
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Erro: TELEGRAM_BOT_TOKEN não configurado no arquivo .env")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        print("📡 Consultando a API do Telegram...")
        print("💡 Certifique-se de ter enviado uma mensagem para o bot primeiro!")
        print()
        
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        
        dados = resposta.json()
        
        if not dados.get('ok'):
            print(f"❌ Erro na API: {dados.get('description', 'Erro desconhecido')}")
            return
        
        updates = dados.get('result', [])
        
        if not updates:
            print("⚠️  Nenhuma mensagem encontrada.")
            print("📝 Envie uma mensagem para o bot primeiro:")
            print("   https://t.me/News_hk_duzeradev_bot")
            return
        
        print("✅ Mensagens encontradas:\n")
        
        chat_ids = set()
        for update in updates:
            message = update.get('message', {})
            chat = message.get('chat', {})
            chat_id = chat.get('id')
            first_name = chat.get('first_name', 'N/A')
            username = chat.get('username', 'N/A')
            
            if chat_id:
                chat_ids.add(chat_id)
                print(f"👤 Nome: {first_name}")
                print(f"   Username: @{username}")
                print(f"   Chat ID: {chat_id}")
                print()
        
        if chat_ids:
            chat_id = list(chat_ids)[0]
            print("=" * 50)
            print(f"🎯 Seu Chat ID é: {chat_id}")
            print("=" * 50)
            print()
            print("📝 Adicione esta linha no arquivo .env:")
            print(f"   TELEGRAM_CHAT_ID={chat_id}")
        
    except requests.RequestException as e:
        print(f"❌ Erro ao fazer requisição: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


if __name__ == "__main__":
    obter_chat_id()

