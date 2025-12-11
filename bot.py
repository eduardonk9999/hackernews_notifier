"""
Script principal do HackerNews Notifier.
Obtém as principais notícias do The Hacker News e envia para o Telegram.
"""

import sys
import io

# Configura encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from scraper import obter_top_noticias
from telegram_sender import enviar_noticias
from datetime import datetime


def main():
    """
    Função principal que orquestra a coleta de notícias e envio para o Telegram.
    """
    print("=" * 50)
    print("🚀 HackerNews Notifier")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 50)
    
    print("\n📡 Coletando notícias do The Hacker News...")
    noticias = obter_top_noticias(quantidade=10)
    
    if not noticias:
        print("❌ Nenhuma notícia foi encontrada. Verifique sua conexão ou a estrutura do site.")
        return
    
    print(f"✅ {len(noticias)} notícias coletadas com sucesso!")
    print("\n📝 Notícias encontradas:")
    for i, noticia in enumerate(noticias, 1):
        print(f"  {i}. {noticia['titulo'][:60]}...")
    
    print("\n📤 Enviando para o Telegram...")
    sucesso = enviar_noticias(noticias)
    
    if sucesso:
        print("\n✅ Processo concluído com sucesso!")
    else:
        print("\n❌ Falha ao enviar mensagem. Verifique as configurações do Telegram.")


if __name__ == "__main__":
    main()

