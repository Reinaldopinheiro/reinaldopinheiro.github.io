# =================================================================
# NOME: Gerador de Boletim Diário (Sem Envio/Interface)
# VERSÃO: 5.5
# AUTOR: Reinaldo Pinheiro & IA Gemini
# DESCRIÇÃO: Gera o arquivo boletim5.html com visual premium e profissional.
# =================================================================

import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
import urllib3

# Desativa os avisos de conexões HTTPS inseguras
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURAÇÕES DE VARIÁVEIS E RODAPÉ ---
VERSION = "5.5"
ARQUIVO_NOME = "boletim5.html"
PIX_KEY = "doe@reinaldopinheiro.com.br"           # Altere para a sua chave PIX real
QRCODE_FILENAME = "qrcode.png"       # Altere para o nome/caminho correto do seu QRCode se houver

def escrever_log(mensagem):
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"[{agora}] {mensagem}")

# --- BUSCA DE DADOS ---

def get_frase_motivacional():
    frases = [
        "A gente só passa por essa vida uma vez, e ainda assim esquecemos de viver.",
        "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
        "Acredite em si mesmo e tudo será possível.",
        "A persistência é o caminho do êxito."
    ]
    dia_do_ano = datetime.now().timetuple().tm_yday
    return frases[dia_do_ano % len(frases)]

def get_horoscopo_rotativo():
    signos = [
        {"nome": "Áries", "slug": "aries"},
        {"nome": "Touro", "slug": "touro"},
        {"nome": "Gêmeos", "slug": "gemeos"},
        {"nome": "Câncer", "slug": "cancer"},
        {"nome": "Leão", "slug": "leao"},
        {"nome": "Virgem", "slug": "virgem"},
        {"nome": "Libra", "slug": "libra"},
        {"nome": "Escorpião", "slug": "escorpiao"},
        {"nome": "Sagitário", "slug": "sagitario"},
        {"nome": "Capricórnio", "slug": "capricornio"},
        {"nome": "Aquário", "slug": "aquario"},
        {"nome": "Peixes", "slug": "peixes"}
    ]
    
    dia_do_ano = datetime.now().timetuple().tm_yday
    signo_hoje = signos[dia_do_ano % len(signos)]
    
    try:
        escrever_log(f"Buscando horóscopo do dia para {signo_hoje['nome']} (Terra)...")
        url = f"https://www.terra.com.br/vida-e-estilo/horoscopo/signos/{signo_hoje['slug']}/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        res = requests.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        paragrafo = soup.find('div', class_='text').find('p')
        texto_previsao = paragrafo.text.strip()
        
        return signo_hoje['nome'], texto_previsao
    except Exception as e:
        escrever_log(f"Aviso no horóscopo ({signo_hoje['nome']}): {e}. Usando frase padrão.")
        return signo_hoje['nome'], "Dia de focar no seu equilíbrio interior, intuição e boas escolhas."

def get_financas():
    try:
        escrever_log("Buscando finanças...")
        res = requests.get("https://api.hgbrasil.com/finance", timeout=5).json()
        d = res['results']['currencies']['USD']['buy']
        e = res['results']['currencies']['EUR']['buy']
        i = res['results']['stocks']['IBOVESPA']['points']
        return f"{d:.2f}".replace('.',','), f"{e:.2f}".replace('.',','), f"{i:,.0f}".replace(',','.')
    except:
        return "5,20", "5,60", "127.000"

def get_clima():
    try:
        escrever_log("Buscensing clima...")
        url = "https://api.open-meteo.com/v1/forecast?latitude=-23.5475&longitude=-46.6361&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=America%2FSao_Paulo"
        res = requests.get(url, timeout=5).json()
        return round(res['daily']['temperature_2m_max'][0]), round(res['daily']['temperature_2m_min'][0]), res['daily']['precipitation_probability_max'][0]
    except:
        return 28, 20, 0

def processar_noticias(url_rss, limite, icone="📰"):
    try:
        res = requests.get(url_rss, timeout=5)
        root = ET.fromstring(res.content)
        noticias = []
        for item in root.findall('.//item')[:limite]:
            titulo = item.find('title').text.split(' - ')[0]
            if titulo.upper().startswith("BR:"): titulo = titulo[3:].strip()
            link = item.find('link').text
            noticias.append(f"<li><span class='news-icon'>{icone}</span> <div class='news-content'><a href='{link}'>{titulo}</a></div></li>")
        return "\n".join(noticias)
    except:
        return "<li>Erro ao carregar notícias.</li>"

# --- GERAÇÃO DO HTML ---

def gerar_boletim_html():
    escrever_log("--- Iniciando Geração do HTML ---")
    agora = datetime.now()
    
    d, e, i = get_financas()
    t_max, t_min, chuva = get_clima()
    noticias_br = processar_noticias("https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419", 7)
    noticias_esporte = processar_noticias("https://news.google.com/rss/search?q=futebol+brasileirao&hl=pt-BR&gl=BR&ceid=BR:pt-419", 6, "⚽")
    nome_signo, texto_signo = get_horoscopo_rotativo()

    html_content = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boletim Diário</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; color: #333; margin: 0; padding: 20px 10px; }}
        .container {{ max-width: 600px; background: #ffffff; margin: 0 auto; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        
        /* Cabeçalho */
        .header {{ text-align: center; margin-bottom: 25px; }}
        .logo {{ max-width: 180px; height: auto; margin-bottom: 10px; }}
        .main-title {{ font-size: 26px; color: #1e293b; margin: 5px 0; font-weight: 700; letter-spacing: -0.5px; }}
        
        /* Saudação Chamativa */
        .welcome-box {{ background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; padding: 18px; border-radius: 8px; text-align: center; margin-bottom: 25px; box-shadow: 0 3px 10px rgba(15,23,42,0.15); }}
        .welcome-box b {{ font-size: 18px; display: block; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; color: #38bdf8; }}
        .welcome-box i {{ font-size: 14px; opacity: 0.9; line-height: 1.4; display: block; }}
        
        /* Seções e Cards */
        .section {{ background: #f8fafc; border-left: 4px solid #3b82f6; padding: 15px; margin-bottom: 20px; border-radius: 0 8px 8px 0; }}
        .section-title {{ font-size: 14px; font-weight: bold; text-transform: uppercase; color: #64748b; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
        .grid-data {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; text-align: center; }}
        .data-card {{ background: #ffffff; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 13px; font-weight: 600; color: #1e293b; }}
        .data-card span {{ display: block; font-size: 11px; color: #64748b; margin-bottom: 4px; font-weight: normal; }}
        
        /* Listas de Notícias */
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ display: flex; align-items: flex-start; gap: 10px; padding: 10px 0; border-bottom: 1px solid #e2e8f0; }}
        li:last-child {{ border-bottom: none; padding-bottom: 0; }}
        .news-icon {{ font-size: 16px; margin-top: 2px; }}
        .news-content a {{ color: #2563eb; text-decoration: none; font-size: 14px; font-weight: 500; line-height: 1.4; }}
        .news-content a:hover {{ text-decoration: underline; color: #1d4ed8; }}
        
        /* Rodapé Solicitado */
        footer {{ margin-top: 35px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; font-size: 12px; color: #64748b; }}
        footer p {{ margin: 0 0 15px 0; }}
        .donate-box {{ background: #fffbeb; border: 1px dashed #f59e0b; padding: 15px; border-radius: 8px; color: #451a03; display: inline-block; max-width: 100%; box-sizing: border-box; }}
        .donate-box strong {{ color: #b45309; font-size: 13px; }}
        .donate-box code {{ background: #fef3c7; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 12px; color: #b45309; word-break: break-all; display: inline-block; margin: 5px 0; }}
        .donate-box img {{ max-width: 140px; height: auto; margin: 10px 0; border: 1px solid #fde68a; border-radius: 4px; }}
        .donate-box span {{ display: block; font-size: 11px; color: #78350f; font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Cabeçalho com Logo Centralizada -->
        <div class="header">
            <img src="logorpc.png" alt="RPC Logo" class="logo"><br>
            <div class="main-title">Boletim Diário</div>
        </div>
        
        <!-- Saudação Chamativa -->
        <div class="welcome-box">
            <b>* BOM DIA * | {agora.day}/{agora.month}</b>
            <i>"{get_frase_motivacional()}"</i>
        </div>
        
        <!-- Mercado Financeiro -->
        <div class="section" style="border-left-color: #10b981;">
            <div class="section-title">📊 Mercado Financeiro</div>
            <div class="grid-data">
                <div class="data-card"><span>Dólar</span>R$ {d}</div>
                <div class="data-card"><span>Euro</span>R$ {e}</div>
                <div class="data-card"><span>Ibovespa</span>{i} pts</div>
            </div>
        </div>
        
        <!-- Previsão do Tempo -->
        <div class="section" style="border-left-color: #06b6d4;">
            <div class="section-title">🌤️ Condições do Tempo</div>
            <div class="grid-data">
                <div class="data-card"><span>Máxima</span>🌡️ {t_max}°C</div>
                <div class="data-card"><span>Mínima</span>🌡️ {t_min}°C</div>
                <div class="data-card"><span>Chuva</span>☔ {chuva}%</div>
            </div>
        </div>
        
        <!-- Horóscopo do Dia -->
        <div class="section" style="border-left-color: #8b5cf6;">
            <div class="section-title">🔮 Horóscopo Diário ({nome_signo})</div>
            <p style="margin: 0; font-size: 13.5px; line-height: 1.5; color: #334155;">{texto_signo}</p>
        </div>
        
        <!-- Notícias Principais -->
        <div class="section" style="border-left-color: #f97316;">
            <div class="section-title">📰 Principais Notícias</div>
            <ul>{noticias_br}</ul>
        </div>
        
        <!-- Esportes -->
        <div class="section" style="border-left-color: #ef4444;">
            <div class="section-title">⚽ Futebol &amp; Brasileirão</div>
            <ul>{noticias_esporte}</ul>
        </div>
        
        <!-- Rodapé Formatado Personalizado -->
        <footer>
          <p>© 2026 Copyright Reinaldo Pinheiro Consultoria com Gemini - Versão {VERSION} (Script Automático)</p>
          <div class="donate-box">
            <strong>🎁 Ajude a criar novos projetos</strong><br>
            Chave PIX: <code>{PIX_KEY}</code><br>
            <img src="{QRCODE_FILENAME}" alt="QRCode PIX Donate" title="Escaneie para doar"><br>
            <span>Aponte a câmera do seu banco para o QRCode</span>
          </div>
        </footer>
    </div>
</body>
</html>"""
    
    with open(ARQUIVO_NOME, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    escrever_log(f"✅ Arquivo salvo com sucesso em: {os.path.abspath(ARQUIVO_NOME)}")

if __name__ == "__main__":
    gerar_boletim_html()