import requests
import os
from datetime import datetime, timezone, timedelta
import re
import json

def get_live_scores():
    url = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/scores-fixtures"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        scores = {}
        matches = re.findall(r'([A-Z]{3})\|([^|]+)\|(\d+)\|FT\|(\d+)\|([A-Z]{3})\|([^|]+)', html)
        for m in matches:
            t1_code, t1_name, s1, s2, t2_code, t2_name = m
            key = f"{t1_name.lower()}v{t2_name.lower()}"
            scores[key] = (s1, s2)
            scores[f"{t1_code.lower()}v{t2_code.lower()}"] = (s1, s2)
            
        if not scores:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a', href=True):
                if '/match-centre/match/' in a['href']:
                    txt = a.get_text(separator='|')
                    p = txt.split('|')
                    if len(p) >= 7:
                        try:
                            s1, s2 = p[2].strip(), p[4].strip()
                            if s1.isdigit() and s2.isdigit():
                                scores[f"{p[1].strip().lower()}v{p[6].strip().lower()}"] = (s1, s2)
                        except: continue
        return scores
    except Exception as e:
        print(f"Erro ao buscar placares: {e}")
        return {}

def gerar_html():
    # 1. Configura fuso horário e captura a data/hora atual da execução
    fuso_brasilia = timezone(timedelta(hours=-3))
    agora = datetime.now(fuso_brasilia).strftime("%d/%m/%Y às %H:%M")
    
    # 2. Busca os placares ao vivo da FIFA
    live_scores = get_live_scores()
    
    # Placares forçados/mockados conforme as regras originais do seu script
    if "belgiumvegypt" not in live_scores:
        live_scores["belgiumvegypt"] = ("1", "1")
    if "spainvcabo verde" not in live_scores:
        live_scores["spainvcabo verde"] = ("0", "0")
    if "swedenvtunisia" not in live_scores:
        live_scores["swedenvtunisia"] = ("5", "1")
        
    # 3. Mapeamento de nomes para o padrão FIFA (mantido do seu código original)
    template_to_fifa = {
        "bélgica": "belgium", "egito": "egypt", "espanha": "spain", "cabo verde": "cabo verde",
        "suécia": "sweden", "tunísia": "tunisia", "méxico": "mexico", "áfrica do sul": "south africa",
        "coreia do sul": "korea republic", "tchéquia": "czechia", "canadá": "canada",
        "bósnia": "bosnia and herzegovina", "brasil": "brazil", "marrocos": "morocco",
        "haiti": "haiti", "escócia": "scotland", "estados unidos": "usa", "paraguai": "paraguay",
        "austrália": "australia", "turquia": "turkey", "alemanha": "germany", "curaçao": "curaçao",
        "costa do marfim": "côte d'ivoire", "equador": "ecuador", "países baixos": "netherlands",
        "japão": "japan", "irã": "iran", "nova zelândia": "new zealand", "arábia saudita": "saudi arabia",
        "uruguai": "uruguay", "frança": "france", "senegal": "senegal", "iraque": "iraq",
        "noruega": "norway", "argentina": "argentina", "argélia": "algeria", "áustria": "austria",
        "jordânia": "jordan", "portugal": "portugal", "rd congo": "dr congo", "uzbequistão": "uzbekistan",
        "colômbia": "colombia", "inglaterra": "england", "croácia": "croatia", "gana": "ghana", "panamá": "panama"
    }
    
    # 4. Localiza e lê o arquivo de template HTML
    template_path = "copa/copa_template.html"
    if not os.path.exists(template_path):
        template_path = os.path.join("copa", "copa_template.html")
        
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # 5. CORREÇÃO CRUCIAL: Salva o placar.json obrigatoriamente dentro da pasta 'copa'
    json_path = "copa/placar.json"
    if not os.path.exists("copa"):
        # Fallback de segurança caso a pasta copa não exista na raiz da execução
        json_path = "placar.json"
        
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(live_scores, jf, ensure_ascii=False, indent=4)
    print(f"✅ Sucesso: O arquivo 'placar.json' foi salvo em: {json_path}")
    
    # 6. Injeta a data de atualização na barra de status do template HTML
    html_final = html.replace("__STATUS_BAR_PLACEHOLDER__", f"Última atualização: {agora}")
    
    # 7. Grava o arquivo HTML final compilado para o usuário acessar
    output_html_path = "copa/copa.html"
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_final)
    print(f"✅ Sucesso: O arquivo HTML final foi atualizado em: {output_html_path}")

if __name__ == "__main__":
    gerar_html()