import requests
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass

# Constantes para os índices das âncoras
SPORT_LEAGUE_IDX = 0
TEAM1_IDX = 1
TEAM2_IDX = 2
PITCHER_IDX = 3
PERIOD_IDX = 4
LINE_TYPE_IDX = 5
PRICE_IDX = 6
SIDE_IDX = 7
TEAM_IDX = 8
SPREAD_IDX = 9

@dataclass
class Item:
    sport_league: str = 'Não encontrado'
    event_date_utc: str = 'Não encontrado'
    team1: str = 'Não encontrado'
    team2: str = 'Não encontrado'
    pitcher: str = 'Não encontrado'
    period: str = 'Não encontrado'
    line_type: str = 'Não encontrado'
    price: str = 'Não encontrado'
    side: str = 'Não encontrado'
    team: str = 'Não encontrado'
    spread: float = 0.0

# Função para extrair informações de uma linha de aposta
def extract_bet_info(bet_line):
    item = Item()
    
    # Encontre todas as âncoras com a classe 'text-muted'
    text_muted = bet_line.find_all('a', class_='text-muted')
    
    # Verifique se há elementos suficientes
    if len(text_muted) >= SPREAD_IDX + 1:
        item.sport_league = text_muted[SPORT_LEAGUE_IDX].get_text().strip()
        item.team1 = text_muted[TEAM1_IDX].get_text().strip()
        item.team2 = text_muted[TEAM2_IDX].get_text().strip()
        item.pitcher = text_muted[PITCHER_IDX].get_text().strip()
        item.period = text_muted[PERIOD_IDX].get_text().strip()
        item.line_type = text_muted[LINE_TYPE_IDX].get_text().strip()
        item.price = text_muted[PRICE_IDX].get_text().strip()
        item.side = text_muted[SIDE_IDX].get_text().strip()
        item.team = text_muted[TEAM_IDX].get_text().strip()
        item.spread = text_muted[SPREAD_IDX].get_text().strip()
    
    return item

# URL da página a ser raspada
url = 'https://veri.bet/odds-picks?filter=upcoming'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

# Realizar uma solicitação GET à página
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    items = []
    
    # Encontrar todas as linhas de apostas na página
    bet_lines = soup.find_all('div', class_='col-lg')
    
    for bet_line in bet_lines:
        item = extract_bet_info(bet_line)
        items.append(item)
    
    # Converter os itens para uma representação JSON
    json_data = json.dumps([item.__dict__ for item in items], ensure_ascii=False, indent=2)
    
    # Imprimir os dados JSON no console
    print(json_data)
else:
    print('Falha ao obter a página.')
