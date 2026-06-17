# ==============================================================================
# PROGRAMA: Central Real-Time Copa do Mundo 2026 - RPC
# VERSÃO: v21.0.0 (REMOVIDO BLOCO DE ESTATÍSTICAS EXTERNAS)
# DATA: 17/06/2026
# AUTOR/MANTENEDOR: Reinaldo Pinheiro Consultoria
# ==============================================================================

import os
import json
import base64
from datetime import datetime, timedelta
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL_API_REALTIME = "https://fixturedownload.com/feed/json/fifa-world-cup-2026"
COPYRIGHT = "Oferecimento: RPC - Reinaldo Pinheiro Consultoria - Ajude a ter novos projetos doando no pix: doe@reinaldopinheiro.com.br"

# Dicionário revisado com os códigos ISO exatos do flag-icons
times_mapeamento = {
    "México": "mx", "África do Sul": "za", "Coreia do Sul": "kr", "Tchéquia": "cz",
    "Canadá": "ca", "Bósnia": "ba", "Catar": "qa", "Suíça": "ch",
    "BRASIL": "br", "Marrocos": "ma", "Haiti": "ht", "Escócia": "gb-sct",
    "Estados Unidos": "us", "Paraguai": "py", "Austrália": "au", "Turquia": "tr",
    "Alemanha": "de", "Curaçao": "cw", "Costa do Marfim": "ci", "Equador": "ec",
    "Países Baixos": "nl", "Japão": "jp", "Suécia": "se", "Tunísia": "tn",
    "Bélgica": "be", "Egito": "eg", "Irã": "ir", "Nova Zelândia": "nz",
    "Espanha": "es", "Cabo Verde": "cv", "Arábia Saudita": "sa", "Uruguai": "uy",
    "França": "fr", "Senegal": "sn", "Iraque": "iq", "Noruega": "no",
    "Argentina": "ar", "Argélia": "dz", "Áustria": "at", "Jordânia": "jo",
    "Portugal": "pt", "RD Congo": "cd", "Uzbequistão": "uz", "Colômbia": "co",
    "Inglaterra": "gb-eng", "Croácia": "hr", "Gana": "gh", "Panamá": "pa"
}

grupos_definidos = {
    "A": ["México", "África do Sul", "Coreia do Sul", "Tchéquia"],
    "B": ["Canadá", "Bósnia", "Catar", "Suíça"],
    "C": ["BRASIL", "Marrocos", "Haiti", "Escócia"],
    "D": ["Estados Unidos", "Paraguai", "Austrália", "Turquia"],
    "E": ["Alemanha", "Curaçao", "Costa do Marfim", "Equador"],
    "F": ["Países Baixos", "Japão", "Suécia", "Tunísia"],
    "G": ["Bélgica", "Egito", "Irã", "Nova Zelândia"],
    "H": ["Espanha", "Cabo Verde", "Arábia Saudita", "Uruguai"],
    "I": ["França", "Senegal", "Iraque", "Noruega"],
    "J": ["Argentina", "Argélia", "Áustria", "Jordânia"],
    "K": ["Portugal", "RD Congo", "Uzbequistão", "Colômbia"],
    "L": ["Inglaterra", "Croácia", "Gana", "Panamá"]
}

def obter_logo_base64():
    arquivo_logo = "logorpc.png"
    if os.path.exists(arquivo_logo):
        try:
            with open(arquivo_logo, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:image/png;base64,{encoded_string}"
        except Exception as e:
            print(f"⚠️ Erro ao converter o arquivo local logorpc.png: {e}")
    return "https://via.placeholder.com/280x90?text=RPC+Consultoria"

def inicializar_classificacao():
    tabela = {}
    for g, selecoes in grupos_definidos.items():
        tabela[g] = {}
        for nome in selecoes:
            flag = times_mapeamento.get(nome, "un")
            tabela[g][nome] = {"P": 0, "J": 0, "V": 0, "SG": 0, "f": flag, "b": (nome == "BRASIL")}
    return tabela

def traduzir_nome(nome_en):
    if not nome_en: return "A definir"
    traducoes = {
        "Brazil": "BRASIL", "Mexico": "México", "South Africa": "África do Sul", "South Korea": "Coreia do Sul",
        "Czech Republic": "Tchéquia", "Czechia": "Tchéquia", "Canada": "Canadá", "Bosnia and Herzegovina": "Bósnia",
        "Qatar": "Catar", "Switzerland": "Suíça", "Morocco": "Marrocos", "Scotland": "Escócia", 
        "USA": "Estados Unidos", "United States": "Estados Unidos", "Paraguay": "Paraguai", "Australia": "Austrália", 
        "Turkey": "Turquia", "Germany": "Alemanha", "Ivory Coast": "Costa do Marfim", "Ecuador": "Equador", 
        "Netherlands": "Países Baixos", "Japan": "Japão", "Sweden": "Suécia", "Tunisia": "Tunísia", 
        "Belgium": "Bélgica", "Egypt": "Egito", "Iran": "Irã", "New Zealand": "Nova Zelândia", 
        "Spain": "Espanha", "Cape Verde": "Cabo Verde", "Saudi Arabia": "Arábia Saudita", "Uruguay": "Uruguai", 
        "France": "França", "Norway": "Noruega", "Senegal": "Senegal", "Iraq": "Iraque",
        "Argentina": "Argentina", "Algeria": "Argélia", "Austria": "Áustria", "Jordan": "Jordânia",
        "Portugal": "Portugal", "DR Congo": "RD Congo", "Congo DR": "RD Congo", "Uzbekistan": "Uzbequistão", "Colombia": "Colômbia",
        "England": "Inglaterra", "Croatia": "Croácia", "Ghana": "Gana", "Panama": "Panamá"
    }
    return traducoes.get(nome_en.strip(), nome_en.strip())

def extrair_data_hora(string_data):
    if not string_data:
        return "A def.", "16h00"
    try:
        if "T" in string_data:
            dt = datetime.strptime(string_data.split("Z")[0].split("+")[0], "%Y-%m-%dT%H:%M:%S")
        else:
            dt = datetime.strptime(string_data, "%Y-%m-%d")
        dt = dt - timedelta(hours=3)
        return dt.strftime("%d/%m"), dt.strftime("%H:%M")
    except:
        return "A def.", "16h00"

def buscar_dados_reais():
    print("🌐 Sincronizando resultados em tempo real com a API da FIFA...")
    estrutura_copa = {
        "grupos": {1: [], 2: [], 3: []},
        "r32": [], "r16": [], "r8": [], "r4": [], "third": [], "final": []
    }
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL_API_REALTIME, headers=headers, timeout=12, verify=False)
        if response.status_code != 200:
            return (estrutura_copa, False)
            
        dados = response.json()
        for match in dados:
            id_jogo = match.get("MatchNumber")
            t1 = traduzir_nome(match.get("HomeTeam"))
            t2 = traduzir_nome(match.get("AwayTeam"))
            g1 = match.get("HomeTeamScore")
            g2 = match.get("AwayTeamScore")
            
            data_f, hora_f = extrair_data_hora(match.get("DateUtc"))
            grupo_raw = match.get("Group", "")
            grupo_letra = grupo_raw.replace("Group ", "").strip().upper() if grupo_raw else ""
            
            encerrado = (g1 is not None and g2 is not None)
            
            jogo_dict = {
                "num": id_jogo, "data": data_f, "hora": hora_f, "grupo": grupo_letra,
                "t1": t1, "f1": times_mapeamento.get(t1, "un"),
                "t2": t2, "f2": times_mapeamento.get(t2, "un"),
                "est": match.get("Location", "Estádio Oficial FIFA"),
                "g1": int(g1) if encerrado else "", 
                "g2": int(g2) if encerrado else "", 
                "encerrado": encerrado
            }
            
            stage = match.get("RoundNumber", 1)
            if stage == 1: estrutura_copa["grupos"][1].append(jogo_dict)
            elif stage == 2: estrutura_copa["grupos"][2].append(jogo_dict)
            elif stage == 3: estrutura_copa["grupos"][3].append(jogo_dict)
            elif stage == 4: estrutura_copa["r32"].append(jogo_dict)
            elif stage == 5: estrutura_copa["r16"].append(