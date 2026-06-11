import time
import os
from datetime import datetime
import requests  # Biblioteca para buscar os dados na internet
from git import Repo

# ==========================================
# CONFIGURAÇÕES DA API REAL (CHAVE EM CONTA)
# ==========================================
# Sua chave oficial ativa do painel api-football
API_KEY_FUTEBOL = "60a92317a4d108039cf95eb34f443302" 

# ID Oficial da Copa do Mundo da FIFA na API (Geralmente ID 1)
ID_CAMPEONATO_COPA = 1 

# ==========================================
# CONFIGURAÇÕES DO GITHUB
# ==========================================
# Mantendo o padrão para rodar direto na pasta do repositório
CAMINHO_REPOSITORIO_LOCAL = "./"  
BRANCH_GITHUB = "main"

# ==========================================
# METADADOS E INFORMAÇÕES DO APLICATIVO
# ==========================================
VERSAO = "v3.2.1 (Live API RPC Header - Fixed)"
DATA_VERSAO = "11/06/2026"
COPYRIGHT = "© 2026 RPC - Reinaldo Pinheiro Consultoria. Todos os direitos reservados."

# Dicionário de mapeamento para as bandeiras CSS locais
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

def inicializar_classificacao():
    tabela = {}
    for g, selecoes in grupos_definidos.items():
        tabela[g] = {}
        for nome in selecoes:
            flag = times_mapeamento.get(nome, "un")
            is_br = True if nome == "BRASIL" else False
            tabela[g][nome] = {"P": 0, "J": 0, "V": 0, "SG": 0, "f": flag, "b": is_br}
    return tabela

def traduzir_nome_time(nome_en):
    traducoes = {
        "Brazil": "BRASIL", "Mexico": "México", "South Africa": "África do Sul", "South Korea": "Coreia do Sul",
        "Czech Republic": "Tchéquia", "Canada": "Canadá", "Bosnia": "Bósnia", "Qatar": "Catar", "Switzerland": "Suíça",
        "Morocco": "Marrocos", "Scotland": "Escócia", "USA": "Estados Unidos", "Paraguay": "Paraguai", "Australia": "Austrália",
        "Turkey": "Turquia", "Germany": "Alemanha", "Ivory Coast": "Costa do Marfim", "Ecuador": "Equador",
        "Netherlands": "Países Baixos", "Japan": "Japão", "Sweden": "Suécia", "Tunisia": "Tunísia", "Belgium": "Bélgica",
        "Egypt": "Egito", "Iran": "Irã", "New Zealand": "Nova Zelândia", "Spain": "Espanha", "Cape Verde": "Cabo Verde",
        "Saudi Arabia": "Arábia Saudita", "Uruguay": "Uruguai", "France": "França", "Norway": "Noruega", "Argentina": "Argentina",
        "Algeria": "Argélia", "Austria": "Áustria", "Jordan": "Jordânia", "Portugal": "Portugal", "DR Congo": "RD Congo",
        "Uzbekistan": "Uzbequistão", "Colombia": "Colômbia", "England": "Inglaterra", "Croatia": "Croácia", "Ghana": "Gana", "Panama": "Panamá"
    }
    return traducoes.get(nome_en, nome_en)

def buscar_dados_reais_api():
    url = f"https://v3.football.api-sports.io/fixtures?league={ID_CAMPEONATO_COPA}&season=2026"
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': API_KEY_FUTEBOL
    }
    jogos_rodadas = {1: [], 2: [], 3: []}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        dados_api = response.json()
        if "response" not in dados_api or len(dados_api["response"]) == 0:
            return None
        for item in dados_api["response"]:
            fixture = item["fixture"]
            league = item["league"]
            teams = item["teams"]
            goals = item["goals"]
            rodada_str = league.get("round", "")
            rodada_num = 1
            if "2" in rodada_str: rodada_num = 2
            elif "3" in rodada_str: rodada_num = 3
            t1_pt = traduzir_nome_time(teams["home"]["name"])
            t2_pt = traduzir_nome_time(teams["away"]["name"])
            grupo_jogo = "A"
            for g, lista in grupos_definidos.items():
                if t1_pt in lista:
                    grupo_jogo = g
                    break
            dt_objeto = datetime.fromisoformat(fixture["date"].replace("Z", "+00:00"))
            data_formatada = dt_objeto.strftime("%d/%m")
            hora_formatada = dt_objeto.strftime("%Hh%M")
            status = fixture["status"]["short"]
            encerrado_ou_ao_vivo = status in ["FT", "1H", "2H", "HT", "P"]
            g1 = goals["home"] if goals["home"] is not None else ""
            g2 = goals["away"] if goals["away"] is not None else ""
            jogos_rodadas[rodada_num].append({
                "data": data_formatada, "hora": hora_formatada, "grupo": grupo_jogo,
                "t1": t1_pt, "f1": times_mapeamento.get(t1_pt, "un"),
                "t2": t2_pt, "f2": times_mapeamento.get(t2_pt, "un"),
                "est": item["fixture"].get("venue", {}).get("name", "Arena FIFA"),
                "g1": g1, "g2": g2, "encerrado": encerrado_ou_ao_vivo
            })
        return jogos_rodadas
    except Exception as e:
        print(f"❌ Falha ao acessar a API: {e}")
        return None

def atualizar_classificacao(jogos_rodadas):
    classificacao_limpa = inicializar_classificacao()
    if not jogos_rodadas: return classificacao_limpa
    for r in [1, 2, 3]:
        for j in jogos_rodadas[r]:
            if j["encerrado"] and j["g1"] != "" and j["g2"] != "":
                g1, g2 = int(j["g1"]), int(j["g2"])
                grupo = j["grupo"]
                t1, t2 = j["t1"], j["t2"]
                if t1 in classificacao_limpa[grupo] and t2 in classificacao_limpa[grupo]:
                    classificacao_limpa[grupo][t1]["J"] += 1
                    classificacao_limpa[grupo][t2]["J"] += 1
                    classificacao_limpa[grupo][t1]["SG"] += (g1 - g2)
                    classificacao_limpa[grupo][t2]["SG"] += (g2 - g1)
                    if g1 > g2:
                        classificacao_limpa[grupo][t1]["P"] += 3
                        classificacao_limpa[grupo][t1]["V"] += 1
                    elif g2 > g1:
                        classificacao_limpa[grupo][t2]["P"] += 3
                        classificacao_limpa[grupo][t2]["V"] += 1
                    else:
                        classificacao_limpa[grupo][t1]["P"] += 1
                        classificacao_limpa[grupo][t2]["P"] += 1
    return classificacao_limpa

def compilar_html(classificacao, jogos_rodadas):
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Central da Copa do Mundo 2026 - RPC Consultoria</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.2.3/css/flag-icons.min.css"/>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, sans-serif; }}
        body {{ background-color: #f4f6f9; color: #1e293b; padding-bottom: 80px; }}
        header {{
            background-color: #ffffff;
            border-bottom: 3px solid #0d9488;
            padding: 15px 0;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}
        .header-banner {{
            max-width: 100%;
            height: auto;
            max-height: 110px;
            display: block;
            margin: 0 auto;
        }}
        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}
        .tabs-container {{ display: flex; background: #cbd5e1; padding: 4px; border-radius: 8px; margin-bottom: 20px; gap: 4px; }}
        .tab-btn {{ flex: 1; padding: 12px; background: none; border: none; font-size: 14px; font-weight: bold; color: #475569; cursor: pointer; border-radius: 6px; text-align: center; }}
        .tab-btn.active {{ background: #1e3a8a; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .subtabs-container {{ display: flex; background: #e2e8f0; padding: 4px; border-radius: 6px; margin-bottom: 15px; gap: 4px; overflow-x: auto; }}
        .subtab-btn {{ padding: 8px 16px; background: none; border: none; font-size: 12px; font-weight: bold; color: #475569; cursor: pointer; border-radius: 4px; white-space: nowrap; }}
        .subtab-btn.active {{ background: #0d9488; color: white; }}
        .tab-content, .subtab-content {{ display: none; }}
        .tab-content.active, .subtab-content.active {{ display: block; }}
        .status-bar {{ background-color: #ffffff; border-left: 4px solid #0d9488; padding: 12px; margin-bottom: 20px; font-size: 13px; color: #475569; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }}
        .live-indicator {{ display: flex; align-items: center; gap: 6px; font-weight: bold; color: #0d9488; }}
        .pulse {{ width: 8px; height: 8px; background-color: #0d9488; border-radius: 50%; animation: pulse-animation 1.5s infinite; }}
        @keyframes pulse-animation {{ 0% {{ transform: scale(0.9); opacity: 1; }} 50% {{ transform: scale(1.4); opacity: 0.5; }} 100% {{ transform: scale(0.9); opacity: 1; }} }}
        .groups-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .group-card {{ background: white; border-radius: 8px; padding: 15px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border-top: 4px solid #0d9488; }}
        .group-title {{ font-size: 15px; font-weight: bold; color: #1e3a8a; margin-bottom: 10px; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }}
        .table-wrapper {{ background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }}
        th {{ background-color: #1e3a8a; color: white; font-weight: 700; padding: 10px; text-transform: uppercase; }}
        td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; vertical-align: middle; }}
        tr:nth-child(even) td {{ background-color: #f8fafc; }}
        .center {{ text-align: center; }} .right {{ text-align: right; }}
        .c-p {{ font-weight: bold; color: #1e3a8a; }}
        tr.brasil-row td {{ background-color: #f0fdf4 !important; }}
        .date-col {{ font-weight: bold; color: #1e3a8a; }}
        .group-badge {{ background-color: #e2e8f0; color: #334155; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        tr.brasil-row .group-badge {{ background-color: #bbf7d0; color: #166534; }}
        .flag {{ display: inline-block; width: 20px; height: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); border-radius: 2px; vertical-align: middle; margin: 0 4px; }}
        .brasil-text {{ font-weight: bold; color: #047857; }}
        .placar-wrapper {{ display: flex; justify-content: center; align-items: center; gap: 6px; }}
        .score {{ background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center; font-weight: bold; }}
        footer {{ position: fixed; bottom: 0; left: 0; width: 100%; background-color: #ffffff; border-top: 2px solid #e2e8f0; padding: 12px; text-align: center; font-size: 12px; color: #64748b; box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.05); z-index: 1000; }}
        .metadata-box {{ font-size: 11px; color: #94a3b8; margin-top: 4px; }}
    </style>
</head>
<body>

    <header>
        <img src="image_0f6aff.png" alt="RPC Consultoria" class="header-banner">
    </header>

    <div class="container">
        <div class="tabs-container">
            <button class="tab-btn active" onclick="switchMainTab('classificacao', event)">📊 Grupos e Classificação</button>
            <button class="tab-btn" onclick="switchMainTab('jogos-grupo', event)">⚽ Fase de Grupos</button>
            <button class="tab-btn" onclick="switchMainTab('mata-mata', event)">🏆 Fases Eliminatórias</button>
        </div>

        <div class="status-bar">
            <div><strong>Última Sincronização:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</div>
            <div class="live-indicator"><div class="pulse"></div> Publicado em reinaldpinheiro.com.br</div>
        </div>

        <div id="classificacao" class="tab-content active">
            <div class="groups-grid">"""

    for grupo, selecoes in classificacao.items():
        selecoes_ordenadas = sorted(selecoes.items(), key=lambda x: (x[1]["P"], x[1]["SG"]), reverse=True)
        html += f"""
                <div class="group-card">
                    <div class="group-title">Grupo {grupo}</div>
                    <table>
                        <thead><tr><th>Seleção</th><th class="center">P</th><th class="center">J</th><th class="center">SG</th></tr></thead>
                        <tbody>"""
        for nome_sel, dados in selecoes_ordenadas:
            row_class = "class='brasil-row'" if dados["b"] else ""
            txt_class = "class='brasil-text'" if dados["b"] else ""
            html += f"""
                            <tr {row_class}>
                                <td><span class="flag fi fi-{dados['f']}"></span> <span {txt_class}>{nome_sel}</span></td>
                                <td class="center c-p">{dados['P']}</td>
                                <td class="center">{dados['J']}</td>
                                <td class="center">{dados['SG']}</td>
                            </tr>"""
        html += """
                        </tbody>
                    </table>
                </div>"""

    html += """
            </div>
        </div>

        <div id="jogos-grupo" class="tab-content">
            <div class="subtabs-container">
                <button class="subtab-btn active" onclick="switchSubTab('rodada1', event)">1ª Rodada</button>
                <button class="subtab-btn" onclick="switchSubTab('rodada2', event)">2ª Rodada</button>
                <button class="subtab-btn" onclick="switchSubTab('rodada3', event)">3ª Rodada</button>
            </div>"""

    for r in [1, 2, 3]:
        active_class = "active" if r == 1 else ""
        html += f"""
            <div id="rodada{r}" class="subtab-content {active_class}">
                <div class="table-wrapper">
                    <table>
                        <thead><tr><th class="center">Data/Hora</th><th class="center">Grupo</th><th class="right">Seleção 1</th><th class="center">Placar</th><th>Seleção 2</th><th>Estádio</th></tr></thead>
                        <tbody>"""
        if r in jogos_rodadas and jogos_rodadas[r]:
            for j in jogos_rodadas[r]:
                is_br = (j["t1"] == "BRASIL" or j["t2"] == "BRASIL")
                row_class = "class='brasil-row'" if is_br else ""
                t1_class = "class='brasil-text'" if j["t1"] == "BRASIL" else ""
                t2_class = "class='brasil-text'" if j["t2"] == "BRASIL" else ""
                g1_vis = j["g1"] if j["encerrado"] else ""
                g2_vis = j["g2"] if j["encerrado"] else ""
                
                html += f"""
                                <tr {row_class}>
                                    <td class="center date-col">{j["data"]}<br><span style="font-size:11px; font-weight:normal; color:#64748b;">{j["hora"]}</span></td>
                                    <td class="center"><span class="group-badge">{j["grupo"]}</span></td>
                                    <td class="right"><span {t1_class}>{j["t1"]}</span> <span class="flag fi fi-{j['f1']}"></span></td>
                                    <td class="center">
                                        <div class="placar-wrapper">
                                            <div class="score">{g1_vis}</div><span style="color:#94a3b8;">x</span><div class="score">{g2_vis}</div>
                                        </div>
                                    </td>
                                    <td><span class="flag fi fi-{j['f2']}"></span> <span {t2_class}>{j["t2"]}</span></td>
                                    <td style="color:#64748b; font-size:12px;">{j["est"]}</td>
                                </tr>"""
        html += """
                        </tbody>
                    </table>
                </div>
            </div>"""

    html += """
        </div>

        <div id="mata-mata" class="tab-content">
            <div class="subtabs-container">
                <button class="subtab-btn active" onclick="switchSubTab('fase-32', event)">Dezesseis-avos</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-16', event)">Oitavas</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-8', event)">Quartas</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-4', event)">Semifinais</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-final', event)">Final 🏆</button>
            </div>"""
            
    fases_config = [('fase-32', 'fase32-tbody', 16, 'Dezesseis-avos'), ('fase-16', 'fase16-tbody', 8, 'Oitavas'), ('fase-8', 'fase8-tbody', 4, 'Quartas'), ('fase-4', 'fase4-tbody', 2, 'Semifinal')]
    for id_fase, tbody_id, qtd, nome in fases_config:
        act = "active" if id_fase == 'fase-32' else ""
        html += f"""
            <div id="{id_fase}" class="subtab-content {act}">
                <div class="table-wrapper">
                    <table>
                        <tbody id="{tbody_id}">"""
        for k in range(1, qtd+1):
            html += f"""
                            <tr>
                                <td class="center" style="font-weight:bold; color:#0d9488;">{nome} [J{k}]</td>
                                <td class="center">A definir</td>
                                <td class="right">Classificado {2*k-1}</td>
                                <td class="center"><div class="placar-wrapper"><div class="score"></div> x <div class="score"></div></div></td>
                                <td>Classificado {2*k}</td>
                                <td>Arena FIFA</td>
                            </tr>"""
        html += """
                        </tbody>
                    </table>
                </div>
            </div>"""

    html += f"""
            <div id="fase-final" class="subtab-content">
                <div class="table-wrapper">
                    <table>
                        <tbody>
                            <tr>
                                <td class="center" style="font-weight:bold; color:#1e3a8a; background-color:#e0f2fe;">Grande Final 🏆</td>
                                <td class="center" style="background-color:#e0f2fe; font-weight:bold;">19/07 - 17h</td>
                                <td class="right" style="background-color:#e0f2fe; font-weight:bold;"><span class="brasil-text">BRASIL</span> <span class="flag fi fi-br"></span></td>
                                <td class="center" style="background-color:#e0f2fe;"><div class="placar-wrapper"><div class="score" style="border-color:#1e3a8a;"></div> x <div class="score" style="border-color:#1e3a8a;"></div></div></td>
                                <td style="background-color:#e0f2fe; font-weight:bold;">Vencedor Semifinal 2</td>
                                <td style="background-color:#e0f2fe; font-weight:bold;">Nova York / NJ</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <div>{COPYRIGHT}</div>
        <div class="metadata-box">Versão do Painel: {VERSAO} | Atualizado em: {DATA_VERSAO}</div>
    </footer>

    <script>
        function switchMainTab(tabId, event) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
            const primeiraSubAba = document.getElementById(tabId).querySelector('.subtab-btn');
            if (primeiraSubAba) {{ primeiraSubAba.click(); }}
        }}
        function switchSubTab(subTabId, event) {{
            const pai = document.getElementById(subTabId).parentElement;
            pai.querySelectorAll('.subtab-content').forEach(el => el.classList.remove('active'));
            pai.querySelectorAll('.subtab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(subTabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('keydown', e => {{
            if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && ['I','J','C'].includes(e.key.toUpperCase())) || (e.ctrlKey && e.key.toUpperCase() === 'U')) {{
                e.preventDefault();
            }}
        }});
    </script>
</body>
</html>"""
    
    caminho_final = os.path.join(CAMINHO_REPOSITORIO_LOCAL, "copa.html")
    with open(caminho_final, "w", encoding="utf-8") as f:
        f.write(html)

def fazer_upload_github():
    try:
        horario = datetime.now().strftime('%H:%M:%S')
        repo = Repo(CAMINHO_REPOSITORIO_LOCAL)
        repo.git.checkout(BRANCH_GITHUB)
        repo.index.add(["copa.html"])
        if repo.is_dirty(untracked_files=False):
            repo.index.commit(f"API Live Update - {horario}")
            origem = repo.remote(name='origin')
            origem.push(BRANCH_GITHUB)
            print(f"[{horario}] ↑ Site reinaldpinheiro.com.br atualizado com dados reais da API!")
        else:
            print(f"[{horario}] ✅ Arquivo 'copa.html' sem mudanças. Ignorando push.")
    except Exception as e:
        print(f"❌ Erro Git Deploy: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print(f"SISTEMA CONECTADO À API REAL DA COPA 2026")
    print("=" * 60)
    
    while True:
        dados_reais = buscar_dados_reais_api()
        tabela_calculada = atualizar_classificacao(dados_reais)
        compilar_html(tabela_calculada, dados_reais)
        fazer_upload_github()
            
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Dormindo por 60 segundos...")
        time.sleep(60)