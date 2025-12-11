"""
Bot em modo daemon - executa continuamente e envia notícias em intervalos.
Pressione Ctrl+C para parar.
"""

import sys
import io
import time
from datetime import datetime

# Configura encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from scraper import obter_top_noticias
from telegram_sender import enviar_noticias


def main():
    """
    Executa o bot em loop contínuo.
    Por padrão, executa a cada 24 horas (86400 segundos).
    """
    # Intervalo em segundos (padrão: 24 horas = 86400 segundos)
    # Você pode alterar aqui:
    # - 3600 = 1 hora
    # - 7200 = 2 horas
    # - 86400 = 24 horas (1 dia)
    INTERVALO_SEGUNDOS = 86400  # 24 horas
    
    print("=" * 60)
    print("🤖 HackerNews Notifier - Modo Daemon")
    print("=" * 60)
    print(f"⏰ Executando a cada {INTERVALO_SEGUNDOS // 3600} horas")
    print("🛑 Pressione Ctrl+C para parar")
    print("=" * 60)
    print()
    
    contador = 0
    
    try:
        while True:
            contador += 1
            print(f"\n{'='*60}")
            print(f"🔄 Execução #{contador}")
            print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"{'='*60}\n")
            
            # Coleta notícias
            print("📡 Coletando notícias do The Hacker News...")
            noticias = obter_top_noticias(quantidade=10)
            
            if not noticias:
                print("❌ Nenhuma notícia foi encontrada.")
                print(f"⏳ Aguardando {INTERVALO_SEGUNDOS // 3600} horas até a próxima tentativa...\n")
            else:
                print(f"✅ {len(noticias)} notícias coletadas!")
                print("📤 Enviando para o Telegram...")
                sucesso = enviar_noticias(noticias)
                
                if sucesso:
                    print("✅ Mensagem enviada com sucesso!")
                else:
                    print("❌ Falha ao enviar mensagem.")
            
            # Calcula próximo horário de execução
            proxima_execucao = datetime.now().timestamp() + INTERVALO_SEGUNDOS
            proxima_execucao_str = datetime.fromtimestamp(proxima_execucao).strftime('%d/%m/%Y %H:%M:%S')
            
            print(f"\n⏳ Próxima execução: {proxima_execucao_str}")
            print(f"💤 Aguardando {INTERVALO_SEGUNDOS // 3600} horas...\n")
            
            # Aguarda o intervalo
            time.sleep(INTERVALO_SEGUNDOS)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("🛑 Bot interrompido pelo usuário")
        print(f"📊 Total de execuções: {contador}")
        print("=" * 60)
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("🔄 Tentando novamente em 1 hora...")
        time.sleep(3600)
        main()  # Reinicia o loop


if __name__ == "__main__":
    main()

