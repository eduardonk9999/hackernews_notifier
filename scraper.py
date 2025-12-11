import requests
from bs4 import BeautifulSoup
from typing import List, Dict


def obter_top_noticias(quantidade: int = 10) -> List[Dict[str, str]]:
    """
    Obtém as principais notícias do The Hacker News.
    
    Args:
        quantidade: Número de notícias a retornar (padrão: 10)
    
    Returns:
        Lista de dicionários contendo 'titulo' e 'link' de cada notícia
    """
    url = 'https://thehackernews.com/'
    
    try:
        # Headers para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()
        
        soup = BeautifulSoup(resposta.text, 'html.parser')
        noticias = []
        
        # Estratégia 1: Procura por artigos com estrutura comum
        # Tenta encontrar elementos article ou divs com classes comuns
        artigos = soup.find_all(['article', 'div'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['post', 'article', 'story', 'item', 'news']
        ))
        
        # Estratégia 2: Procura por links que contenham títulos
        if not artigos:
            # Procura por links que tenham h2, h3 ou h4 dentro
            links_com_titulos = []
            todos_links = soup.find_all('a', href=True)
            
            for link in todos_links:
                # Verifica se o link tem um título dentro
                titulo_tag = link.find(['h2', 'h3', 'h4', 'span'], class_=lambda x: x and 'title' in x.lower() if x else False)
                if not titulo_tag:
                    titulo_tag = link.find(['h2', 'h3', 'h4'])
                
                if titulo_tag:
                    titulo = titulo_tag.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if titulo and href and len(titulo) > 15:
                        # Normaliza o link
                        if not href.startswith('http'):
                            if href.startswith('/'):
                                href = 'https://thehackernews.com' + href
                            else:
                                href = 'https://thehackernews.com/' + href
                        
                        # Filtra links que são realmente artigos
                        if 'thehackernews.com' in href and href not in ['https://thehackernews.com/', 'https://thehackernews.com']:
                            noticias.append({
                                'titulo': titulo,
                                'link': href
                            })
        
        # Estratégia 3: Se encontrou artigos, extrai título e link de cada um
        if artigos:
            for artigo in artigos:
                # Procura título
                titulo_tag = artigo.find(['h2', 'h3', 'h4', 'a'], class_=lambda x: x and 'title' in x.lower() if x else False)
                if not titulo_tag:
                    titulo_tag = artigo.find(['h2', 'h3', 'h4'])
                
                # Procura link
                link_tag = artigo.find('a', href=True)
                
                if titulo_tag and link_tag:
                    titulo = titulo_tag.get_text(strip=True)
                    href = link_tag.get('href', '')
                    
                    if titulo and href and len(titulo) > 15:
                        # Normaliza o link
                        if not href.startswith('http'):
                            if href.startswith('/'):
                                href = 'https://thehackernews.com' + href
                            else:
                                href = 'https://thehackernews.com/' + href
                        
                        if 'thehackernews.com' in href:
                            noticias.append({
                                'titulo': titulo,
                                'link': href
                            })
        
        # Remove duplicatas baseado no link
        noticias_unicas = []
        links_vistos = set()
        for noticia in noticias:
            link = noticia['link']
            # Remove parâmetros de query para evitar duplicatas
            link_base = link.split('?')[0].split('#')[0]
            if link_base not in links_vistos:
                noticias_unicas.append(noticia)
                links_vistos.add(link_base)
        
        return noticias_unicas[:quantidade]
        
    except requests.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")
        return []
    except Exception as e:
        print(f"Erro ao processar notícias: {e}")
        return []

