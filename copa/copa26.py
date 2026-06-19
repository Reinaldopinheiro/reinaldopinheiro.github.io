# ==============================================================================
# PROGRAMA: Central Real-Time Copa do Mundo 2026 - RPC
# VERSÃO: v26.4.0 (CORREÇÃO DE PARSING DE DATA COM ESPAÇOS EM BRASÍLIA)
# DATA: 19/06/2026
# AUTOR: Reinaldo Pinheiro Consultoria com Gemini
# ==============================================================================

import os
import json
import base64
from datetime import datetime
import requests
import pytz
import urllib3

# Desativa avisos de SSL para evitar falhas no ambiente do GitHub Actions
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VERSION = "26.4.0"
URL_API_REALTIME = "https://fixturedownload.com/feed/json/fifa-world-cup-2026"
pix_key = "doe@reinaldopinheiro.com.br"
qrcode_filename = "qrcode.png"  # Certifique-se de que este arquivo existe na mesma pasta do HTML

# Mapeamento oficial dos países para os ícones de bandeiras (flag-icons)
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
    if not os.path.exists(arquivo_logo):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        arquivo_logo = os.path.join(diretorio_atual, "logorpc.png")
        
    if os.path.exists(arquivo_logo):
        try:
            with open(arquivo_logo, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:image/png;base64,{encoded_string}"
        except Exception as e:
            print(f"⚠️ Erro ao ler logorpc.png: {e}")
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
        "Brazil": "BRASIL", "Brasil": "BRASIL",
        "Mexico": "México", "South Africa": "África do Sul", 
        "Korea Republic": "Coreia do Sul", "South Korea": "Coreia do Sul",
        "Czech Republic": "Tchéquia", "Czechia": "Tchéquia", 
        "Canada": "Canadá", "Bosnia and Herzegovina": "Bósnia", "Bosnia": "Bósnia",
        "Qatar": "Catar", "Switzerland": "Suíça", "Morocco": "Marrocos", "Scotland": "Escócia", 
        "USA": "Estados Unidos", "United States": "Estados Unidos", "Paraguay": "Paraguai", "Australia": "Austrália", 
        "Turkey": "Turquia", "Türkiye": "Turquia",
        "Germany": "Alemanha", "Curaçao": "Curaçao", "Côte d'Ivoire": "Costa do Marfim", "Ivory Coast": "Costa do Marfim", "Ecuador": "Equador", 
        "Netherlands": "Países Baixos", "Japan": "Japão", "Sweden": "Suécia", "Tunisia": "Tunísia", 
        "Belgium": "Bélgica", "Egypt": "Egito", "Iran": "Irã", "IR Iran": "Irã", "New Zealand": "Nova Zelândia", 
        "Spain": "Espanha", "Cape Verde": "Cabo Verde", "Saudi Arabia": "Arábia Saudita", "Uruguay": "Uruguai", 
        "France": "França", "Norway": "Noruega", "Senegal": "Senegal", "Iraq": "Iraque",
        "Argentina": "Argentina", "Algeria": "Argélia", "Austria": "Áustria", "Jordan": "Jordânia",
        "Portugal": "Portugal", "DR Congo": "RD Congo", "Congo DR": "RD Congo", "Uzbekistan": "Uzbequistão", "Colombia": "Colômbia",
        "England": "Inglaterra", "Croatia": "Croácia", "Ghana": "Gana", "Panama": "Panamá"
    }
    return traducoes.get(nome_en.strip(), nome_en.strip())

def extrair_data_hora(string_data):
    if not string_data:
        return "A def.", "A def."
    try:
        # Substitui espaços por 'T' para que a string de data sempre siga o padrão ISO limpo
        data_limpa = string_data.split(".")[0].strip().replace(" ", "T")
        if data_limpa.endswith("Z"):
            data_limpa = data_limpa[:-1] + "+00:00"
            
        if "T" in data_limpa:
            if "+" in data_limpa or "-" in data_limpa[10:]:
                dt = datetime.strptime(data_limpa, "%Y-%m-%dT%H:%M:%S%z")
            else:
                dt = datetime.strptime(data_limpa, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.utc)
        else:
            dt = datetime.strptime(data_limpa, "%Y-%m-%d").replace(tzinfo=pytz.utc)
            
        # Converte para o fuso horário oficial de Brasília
        fuso_brasilia = pytz.timezone("America/Sao_Paulo")
        dt_br = dt.astimezone(fuso_brasilia)
        return dt_br.strftime("%d/%m"), dt_br.strftime("%H:%M")
    except Exception as e:
        print(f"⚠️ Falha ao processar data '{string_data}': {e}")
        return "A def.", "A def."

def buscar_dados_reais():
    print("🌐 Baixando dados oficiais da FIFA em tempo real...")
    estrutura_copa = {
        "grupos": [], "r32": [], "r16": [], "r8": [], "r4": [], "third": [], "final": []
    }
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL_API_REALTIME, headers=headers, timeout=15, verify=False)
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
            
            stage_number = match.get("RoundNumber", 1)
            
            if stage_number == 1 or grupo_letra:
                estrutura_copa["grupos"].append(jogo_dict)
            elif stage_number == 2: estrutura_copa["r32"].append(jogo_dict)
            elif stage_number == 3: estrutura_copa["r16"].append(jogo_dict)
            elif stage_number == 4: estrutura_copa["r8"].append(jogo_dict)
            elif stage_number == 5: estrutura_copa["r4"].append(jogo_dict)
            elif stage_number == 6: estrutura_copa["third"].append(jogo_dict)
            elif stage_number == 7: estrutura_copa["final"].append(jogo_dict)

        return (estrutura_copa, True)
    except Exception as e:
        print(f"❌ Erro ao ler a API: {e}")
        return (estrutura_copa, False)

def atualizar_classificacao(estrutura_copa):
    classificacao_limpa = inicializar_classificacao()
    for j in estrutura_copa["grupos"]:
        if j["encerrado"]:
            g1, g2 = int(j["g1"]), int(j["g2"])
            t1, t2 = j["t1"], j["t2"]
            grupo = j["grupo"]
            
            if grupo in classificacao_limpa:
                if t1 in classificacao_limpa[grupo] and t2 in classificacao_limpa[grupo]:
                    classificacao_limpa[grupo][t1]["J"] += 1
                    classificacao_limpa[grupo][t2]["J"] += 1
                    classificacao_limpa[grupo][t1]["SG"] += (g1 - g2)
                    classificacao_limpa[grupo][t2]["SG"] += (g2 - g1)
                    
                    if g1 > g2: 
                        classificacao_limpa[grupo][t1]["P"] += 3
                    elif g2 > g1: 
                        classificacao_limpa[grupo][t2]["P"] += 3
                    else:
                        classificacao_limpa[grupo][t1]["P"] += 1
                        classificacao_limpa[grupo][t2]["P"] += 1
    return classificacao_limpa

def renderizar_tabela_jogos(lista_jogos):
    if not lista_jogos:
        return "<tr><td colspan='6' class='center' style='color:#64748b; padding:20px;'>Aguardando definições oficiais da FIFA.</td></tr>"
    html_jogos = ""
    for j in sorted(lista_jogos, key=lambda x: x['num']):
        is_br = (j["t1"] == "BRASIL" or j["t2"] == "BRASIL")
        row_class = "class='brasil-row'" if is_br else ""
        t1_class = "class='brasil-text'" if j["t1"] == "BRASIL" else ""
        t2_class = "class='brasil-text'" if j["t2"] == "BRASIL" else ""
        
        placar_1 = j["g1"] if j["encerrado"] else "-"
        placar_2 = j["g2"] if j["encerrado"] else "-"
        
        badge_vis = f"<span class='group-badge'>Grupo {j['grupo']}</span>" if j["grupo"] else f"<span class='group-badge fase'>Jogo {j['num']}</span>"
        
        html_jogos += f"""
        <tr {row_class}>
            <td class="center date-col">{j["data"]}<br><span style="font-size:11px; font-weight:normal; color:#64748b;">{j["hora"]}</span></td>
            <td class="center">{badge_vis}</td>
            <td class="right"><span {t1_class}>{j["t1"]}</span> <span class="flag fi fi-{j['f1']}"></span></td>
            <td class="center">
                <div class="placar-wrapper">
                    <div class="score">{placar_1}</div><span style="color:#94a3b8;">x</span><div class="score">{placar_2}</div>
                </div>
            </td>
            <td><span class="flag fi fi-{j['f2']}"></span> <span {t2_class}>{j["t2"]}</span></td>
            <td style="color:#64748b; font-size:12px;">{j["est"]}</td>
        </tr>"""
    return html_jogos

def compiling_html(classificacao, estrutura_copa, status_conexao):
    fuso_br = pytz.timezone("America/Sao_Paulo")
    data_site = datetime.now(fuso_br).strftime('%d/%m/%Y às %H:%M:%S (Brasília)')
    
    cor_status = "#0d9488" if status_conexao else "#ef4444"
    txt_status = "● Dados Oficiais FIFA Atualizados" if status_conexao else "● Erro de sincronização"
    logo_src = obter_logo_base64()

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Central de Resultados Copa do Mundo 2026 - RPC</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.2.3/css/flag-icons.min.css"/>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, sans-serif; }}
        body {{ background-color: #f4f6f9; color: #1e293b; padding-bottom: 240px; }}
        header {{ background-color: #ffffff; border-bottom: 3px solid #0d9488; padding: 15px 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        .header-top-row {{ display: flex; align-items: center; justify-content: space-between; max-width: 1000px; margin: 0 auto; padding: 0 20px; }}
        .header-flag-side {{ width: 50px; height: 35px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); border-radius: 4px; }}
        
        .title-container {{ display: flex; align-items: center; justify-content: center; gap: 15px; margin-top: 5px; }}
        .title-logo {{ max-height: 45px; width: auto; object-fit: contain; }}
        .main-title {{ font-size: 24px; font-weight: 800; color: #1e3a8a; letter-spacing: 1px; text-transform: uppercase; }}
        
        .version-badge {{ text-align: center; margin-top: 4px; font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }}
        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}
        .tabs-container {{ display: flex; background: #cbd5e1; padding: 4px; border-radius: 8px; margin-bottom: 20px; gap: 4px; overflow-x: auto; }}
        .tab-btn {{ flex: 1; padding: 12px; background: none; border: none; font-size: 13px; font-weight: bold; color: #475569; cursor: pointer; border-radius: 6px; text-align: center; white-space: nowrap; }}
        .tab-btn.active {{ background: #1e3a8a; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .subtabs-container {{ display: flex; background: #e2e8f0; padding: 4px; border-radius: 6px; margin-bottom: 15px; gap: 4px; overflow-x: auto; }}
        .subtab-btn {{ padding: 8px 16px; background: none; border: none; font-size: 12px; font-weight: bold; color: #475569; cursor: pointer; border-radius: 4px; white-space: nowrap; }}
        .subtab-btn.active {{ background: #0d9488; color: white; }}
        .tab-content, .subtab-content {{ display: none; }}
        .tab-content.active, .subtab-content.active {{ display: block; }}
        .status-bar {{ background-color: #ffffff; border-left: 4px solid {cor_status}; padding: 12px; margin-bottom: 20px; font-size: 13px; color: #475569; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }}
        .groups-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }}
        .group-card {{ background: white; border-radius: 8px; padding: 15px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border-top: 4px solid #0d9488; }}
        .group-title {{ font-size: 14px; font-weight: bold; color: #1e3a8a; margin-bottom: 10px; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }}
        .table-wrapper {{ background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; overflow-x:auto; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }}
        th {{ background-color: #1e3a8a; color: white; font-weight: 700; padding: 10px; text-transform: uppercase; }}
        td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; vertical-align: middle; }}
        tr:nth-child(even) td {{ background-color: #f8fafc; }}
        .center {{ text-align: center; }} .right {{ text-align: right; }}
        .c-p {{ font-weight: bold; color: #1e3a8a; }}
        tr.brasil-row td {{ background-color: #f0fdf4 !important; }}
        .date-col {{ font-weight: bold; color: #1e3a8a; }}
        .group-badge {{ background-color: #e2e8f0; color: #334155; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        .group-badge.fase {{ background-color: #fee2e2; color: #991b1b; }}
        .flag {{ inline-block; width: 20px; height: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); border-radius: 2px; vertical-align: middle; margin: 0 4px; }}
        .brasil-text {{ font-weight: bold; color: #047857; }}
        .placar-wrapper {{ display: flex; justify-content: center; align-items: center; gap: 6px; }}
        .score {{ background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center; font-weight: bold; }}
        
        /* Estilos do rodapé com caixa de doação */
        footer {{ position: fixed; bottom: 0; left: 0; width: 100%; background-color: #1e3a8a; color: #ffffff; padding: 15px 20px; text-align: center; font-size: 13px; font-weight: 500; z-index: 1000; box-shadow: 0 -4px 10px rgba(0,0,0,0.1); }}
        footer p {{ margin-bottom: 8px; color: #e2e8f0; }}
        .donate-box {{ background: rgba(255, 255, 255, 0.1); border: 1px dashed rgba(255, 255, 255, 0.3); border-radius: 6px; padding: 8px; display: inline-block; max-width: 400px; font-size: 11px; }}
        .donate-box strong {{ font-size: 12px; color: #fde047; }}
        .donate-box code {{ background: #0f172a; padding: 2px 6px; border-radius: 4px; font-family: monospace; color: #38bdf8; font-size: 12px; }}
        .donate-box img {{ height: 55px; width: auto; margin: 4px 0; border-radius: 4px; background: white; padding: 2px; vertical-align: middle; }}
        .donate-box span {{ color: #cbd5e1; display: block; margin-top: 2px; }}
    </style>
</head>
<body>
    <header>
        <div class="header-top-row">
            <div style="width: 50px;"></div>
            
            <div class="title-container">
                <img src="{logo_src}" alt="RPC Consultoria" class="title-logo">
                <h1 class="main-title">Central de Resultados Copa 2026</h1>
            </div>
            
            <div><span class="flag fi fi-br header-flag-side"></span></div>
        </div>
        <div class="version-badge">Versão do Sistema: {VERSION}</div>
    </header>
    
    <div class="container">
        <div class="tabs-container">
            <button class="tab-btn active" onclick="switchMainTab('classificacao', event)">📊 Classificação dos Grupos</button>
            <button class="tab-btn" onclick="switchMainTab('jogos-grupo', event)">📅 Todos os Jogos da Fase de Grupos</button>
            <button class="tab-btn" onclick="switchMainTab('eliminatorias', event)">🏆 Fases Eliminatórias</button>
        </div>

        <div class="status-bar">
            <div><strong>Última Atualização:</strong> {data_site}</div>
            <div style="font-weight: bold; color: {cor_status};">{txt_status}</div>
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
        for nome_sel, d in selecoes_ordenadas:
            row_class = "class='brasil-row'" if d["b"] else ""
            txt_class = "class='brasil-text'" if d["b"] else ""
            html += f"""
                            <tr {row_class}>
                                <td><span class="flag fi fi-{d['f']}"></span> <span {txt_class}>{nome_sel}</span></td>
                                <td class="center c-p">{d['P']}</td>
                                <td class="center">{d['J']}</td>
                                <td class="center">{d['SG']}</td>
                            </tr>"""
        html += """
                        </tbody>
                    </table>
                </div>"""

    html += f"""
            </div>
        </div>

        <div id="jogos-grupo" class="tab-content">
            <div class="table-wrapper">
                <table>
                    <tbody>
                        {renderizar_tabela_jogos(estrutura_copa["grupos"])}
                    </tbody>
                </table>
            </div>
        </div>

        <div id="eliminatorias" class="tab-content">
            <div class="subtabs-container">
                <button class="subtab-btn active" onclick="switchSubTab('fase-32', event)">Dezesseis-avos</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-16', event)">Oitavas</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-8', event)">Quartas</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-4', event)">Semifinais</button>
                <button class="subtab-btn" onclick="switchSubTab('fase-finais', event)">Finais 🏆</button>
            </div>
            <div id="fase-32" class="subtab-content active"><div class="table-wrapper"><table><tbody>{renderizar_tabela_jogos(estrutura_copa["r32"])}</tbody></table></div></div>
            <div id="fase-16" class="subtab-content"><div class="table-wrapper"><table><tbody>{renderizar_tabela_jogos(estrutura_copa["r16"])}</tbody></table></div></div>
            <div id="fase-8" class="subtab-content"><div class="table-wrapper"><table><tbody>{renderizar_tabela_jogos(estrutura_copa["r8"])}</tbody></table></div></div>
            <div id="fase-4" class="subtab-content"><div class="table-wrapper"><table><tbody>{renderizar_tabela_jogos(estrutura_copa["r4"])}</tbody></table></div></div>
            <div id="fase-finais" class="subtab-content">
                <h3 style="margin:10px 0; color:#1e3a8a; font-size:15px;">Disputa do Terceiro Lugar</h3>
                <div class="table-wrapper"><table><tbody>{renderizar_tabela_jogos(estrutura_copa["third"])}</tbody></table></div>
                <h3 style="margin:10px 0; color:#1e3a8a; font-size:15px;">Grande Final</h3>
                <div class="table-wrapper"><table><tbody>{renderizar_tabela_jogos(estrutura_copa["final"])}</tbody></table></div>
            </div>
        </div>
    </div>

    {{html_footer_content}}

    <script>
        function switchMainTab(tabId, event) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}
        function switchSubTab(subTabId, event) {{
            const pai = document.getElementById(subTabId).parentElement;
            pai.querySelectorAll('.subtab-content').forEach(el => el.classList.remove('active'));
            pai.querySelectorAll('.subtab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(subTabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}
    </script>
</body>
</html>"""

    html_footer_formatted = f"""<footer>
  <p>© 2026 Copyright Reinaldo Pinheiro Consultoria com Gemini - Versão {VERSION} (Script Automático)</p>
  <div class="donate-box">
    <strong>🎁 Ajude a criar novos projetos</strong><br>
    Chave PIX: <code>{pix_key}</code><br>
    <img src="{qrcode_filename}" alt="QRCode PIX Donate" title="Escaneie para doar"><br>
    <span>Aponte a câmera do seu banco para o QRCode</span>
  </div>
</footer>"""

    final_html_page = html.replace("{html_footer_content}", html_footer_formatted)

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(diretorio_atual, "copa26.html")
    caminho_json = os.path.join(diretorio_atual, "placar.json")

    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(final_html_page)
        
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump({
            "atualizado_em": data_site, 
            "classificacao": classificacao, 
            "jogos": estrutura_copa
        }, f, ensure_ascii=False, indent=4)
        
    print(f"✨ Pronto! Página gerada com sucesso com fuso corrigido e sem erros de parsing.")

if __name__ == "__main__":
    estrutura_dados, sucesso = buscar_dados_reais()
    tabela_calculada = atualizar_classificacao(estrutura_dados)
    compiling_html(tabela_calculada, estrutura_dados, status_conexao=sucesso)