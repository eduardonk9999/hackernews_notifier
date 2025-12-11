import requests
from typing import List, Dict
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def formatar_mensagem(noticias: List[Dict[str, str]]) -> str:
    """
    Formata a lista de notícias em uma mensagem bonita para o Telegram.
    
    Args:
        noticias: Lista de dicionários com 'titulo' e 'link'
    
    Returns:
        String formatada com as notícias
    """
    if not noticias:
        return "❌ Não foi possível obter notícias no momento."
    
    mensagem = "📰 <b>Top Notícias do The Hacker News</b>\n\n"
    
    for i, noticia in enumerate(noticias, 1):
        titulo = noticia.get('titulo', 'Sem título')
        link = noticia.get('link', '#')
        
        # Escapa caracteres especiais do HTML
        titulo = titulo.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        mensagem += f"{i}. <b>{titulo}</b>\n"
        mensagem += f"🔗 <a href=\"{link}\">{link}</a>\n\n"
    
    return mensagem


def enviar_mensagem(mensagem: str) -> bool:
    """
    Envia uma mensagem para o Telegram.
    
    Args:
        mensagem: Texto da mensagem a ser enviada
    
    Returns:
        True se enviou com sucesso, False caso contrário
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Erro: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não configurados!")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': mensagem,
        'parse_mode': 'HTML'
    }
    
    try:
        resposta = requests.post(url, json=payload, timeout=10)
        resposta.raise_for_status()
        
        resultado = resposta.json()
        if resultado.get('ok'):
            print("✅ Mensagem enviada com sucesso para o Telegram!")
            return True
        else:
            print(f"❌ Erro ao enviar mensagem: {resultado.get('description', 'Erro desconhecido')}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Erro ao fazer requisição para o Telegram: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def enviar_noticias(noticias: List[Dict[str, str]]) -> bool:
    """
    Formata e envia notícias para o Telegram.
    
    Args:
        noticias: Lista de dicionários com 'titulo' e 'link'
    
    Returns:
        True se enviou com sucesso, False caso contrário
    """
    mensagem = formatar_mensagem(noticias)
    return enviar_mensagem(mensagem)

