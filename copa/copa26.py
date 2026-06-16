import requests
import os
from datetime import datetime, timezone, timedelta
import json
import unicodedata

def normalizar_nome(txt):
    """ Remove acentos, deixa tudo em minúsculo e limpa espaços """
    if not txt:
        return ""
    origin = str(txt).lower().strip()
    # Remove acentos (ex: 'méxico' vira 'mexico')
    nfkd = unicodedata.normalize('NFKD', origin)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def get_live_scores():
    url = "https://fixturedownload.com/feed/json/fifa-world-cup-2026"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    scores = {}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            for jogo in response.json():
                home_score = jogo.get('HomeTeamScore')
                away_score = jogo.get('AwayTeamScore')
                
                if home_score is not None and away_score is not None:
                    t1 = normalizar_nome(jogo.get('HomeTeam'))
                    t2 = normalizar_nome(jogo.get('AwayTeam'))
                    
                    # Salva das duas formas possíveis para o JS achar não importa a ordem
                    scores[f"{t1}v{t2}"] = (str(home_score), str(away_score))
                    scores[f"{t2}v{t1}"] = (str(away_score), str(home_score))
            print(f"⚽ Sucesso: {len(scores) // 2} placares mapeados de forma bidirecional.")
            return scores
    except Exception as e:
        print(f"Erro na API: {e}")
    return scores

def gerar_html():
    fuso_brasilia = timezone(timedelta(hours=-3))
    agora = datetime.now(fuso_brasilia).strftime("%d/%m/%Y às %H:%M")
    
    live_scores = get_live_scores()
    
    if not os.path.exists("copa"):
        os.makedirs("copa")
    with open("copa/placar.json", "w", encoding="utf-8") as jf:
        json.dump(live_scores, jf, ensure_ascii=False, indent=4)
        
    with open("copa/copa_template.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    html_final = html.replace("__STATUS_BAR_PLACEHOLDER__", f"Última atualização: {agora}")
    
    # Injeta os dados na memória do HTML
    dados_colados = f"\n<script>const PLACARES_LIVE_SERVIDORE = {json.dumps(live_scores)};</script>\n"
    html_final = html_final.replace("<body>", f"<body>{dados_colados}")
    
    with open("copa/copa.html", "w", encoding="utf-8") as f:
        f.write(html_final)
    print("✅ HTML atualizado com sucesso!")

if __name__ == "__main__":
    gerar_html()