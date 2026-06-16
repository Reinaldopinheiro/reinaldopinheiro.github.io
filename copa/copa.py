import requests
import os
from datetime import datetime, timezone, timedelta
import json

def get_live_scores():
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
                
                # Só processa se o jogo já tiver placar (não for nulo)
                if home_score is not None and away_score is not None:
                    # Deixa em minúsculo e remove espaços extras das pontas
                    t1_name = str(jogo.get('HomeTeam')).lower().strip()
                    t2_name = str(jogo.get('AwayTeam')).lower().strip()
                    
                    # Cria a chave direta "time1vtime2"
                    key = f"{t1_name}v{t2_name}"
                    scores[key] = (str(home_score), str(away_score))
            print(f"⚽ Sucesso! {len(scores)} placares processados.")
            return scores
    except Exception as e:
        print(f"Erro na API principal: {e}")
        
    return scores

def gerar_html():
    fuso_brasilia = timezone(timedelta(hours=-3))
    agora = datetime.now(fuso_brasilia).strftime("%d/%m/%Y às %H:%M")
    
    live_scores = get_live_scores()
    
    if not os.path.exists("copa"):
        os.makedirs("copa")
    with open("copa/placar.json", "w", encoding="utf-8") as jf:
        json.dump(live_scores, jf, ensure_ascii=False, indent=4)
        
    template_path = "copa/copa_template.html"
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html_final = html.replace("__STATUS_BAR_PLACEHOLDER__", f"Última atualização: {agora}")
    
    # Injeta os dados limpos na memória do HTML
    dados_colados = f"\n<script>const PLACARES_LIVE_SERVIDORE = {json.dumps(live_scores)};</script>\n"
    html_final = html_final.replace("<body>", f"<body>{dados_colados}")
    
    output_html_path = "copa/copa.html"
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_final)
    print("✅ HTML atualizado com sucesso!")

if __name__ == "__main__":
    gerar_html()