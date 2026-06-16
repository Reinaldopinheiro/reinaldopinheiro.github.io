import requests
import os
from datetime import datetime, timezone, timedelta
import json

def get_live_scores():
    """
    Busca os dados de jogos e placares diretamente de uma API/feed de dados 
    esportivos atualizado para a Copa do Mundo 2026.
    """
    url = "https://fixturedownload.com/feed/json/fifa-world-cup-2026"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    scores = {}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            dados_jogos = response.json()
            for jogo in dados_jogos:
                home_score = jogo.get('HomeTeamScore')
                away_score = jogo.get('AwayTeamScore')
                
                if home_score is not None and away_score is not None:
                    t1_name = str(jogo.get('HomeTeam')).lower().strip()
                    t2_name = str(jogo.get('AwayTeam')).lower().strip()
                    
                    # Formato chave esperado: "time1vtime2"
                    key = f"{t1_name}v{t2_name}"
                    scores[key] = (str(home_score), str(away_score))
            print(f"⚽ Sucesso! {len(scores)} placares dinâmicos obtidos da API principal.")
            return scores
    except Exception as e:
        print(f"Erro na API principal: {e}. Tentando contingência...")
        
    # CONTINGÊNCIA: Caso a API principal falhe
    try:
        url_fallback = "https://raw.githubusercontent.com/openfootball/world-cup/master/2026/cup.json"
        res = requests.get(url_fallback, timeout=10)
        if res.status_code == 200:
            data = res.json()
            for r in data.get('rounds', []):
                for m in r.get('matches', []):
                    if m.get('score') is not None:
                        t1 = m['team1'].lower().strip()
                        t2 = m['team2'].lower().strip()
                        s1 = str(m['score']['fulltime'][0])
                        s2 = str(m['score']['fulltime'][1])
                        scores[f"{t1}v{t2}"] = (s1, s2)
            return scores
    except Exception as e:
        print(f"Erro na contingência: {e}")

    return scores

def gerar_html():
    # 1. Configura fuso horário de Brasília
    fuso_brasilia = timezone(timedelta(hours=-3))
    agora = datetime.now(fuso_brasilia).strftime("%d/%m/%Y às %H:%M")
    
    # 2. Coleta os placares dinâmicos
    live_scores = get_live_scores()
    
    # 3. Mantém uma cópia física do json na pasta copa por garantia
    if not os.path.exists("copa"):
        os.makedirs("copa")
    with open("copa/placar.json", "w", encoding="utf-8") as jf:
        json.dump(live_scores, jf, ensure_ascii=False, indent=4)
        
    # 4. Lê o arquivo de template HTML
    template_path = "copa/copa_template.html"
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # 5. Injeta a data de atualização na barra superior esquerda
    html_final = html.replace("__STATUS_BAR_PLACEHOLDER__", f"Última atualização: {agora}")
    
    # 6. INJEÇÃO DIRETA: Coloca os dados da API na memória do HTML (Evita erros de carregamento)
    dados_colados = f"\n<script>const PLACARES_LIVE_SERVIDORE = {json.dumps(live_scores)};</script>\n"
    html_final = html_final.replace("<body>", f"<body>{dados_colados}")
    
    # 7. Grava o HTML final de exibição
    output_html_path = "copa/copa.html"
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_final)
    print(f"✅ Sucesso: O arquivo HTML final foi gerado em: {output_html_path}")

if __name__ == "__main__":
    gerar_html()