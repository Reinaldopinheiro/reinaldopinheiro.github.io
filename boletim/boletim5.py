# =================================================================
# NOME: Gerador de Boletim Diário (Sem Envio/Interface)
# VERSÃO: 5.4
# AUTOR: Reinaldo Pinheiro & IA Gemini
# DESCRIÇÃO: Gera o arquivo boletim5.html variando o signo do dia.
# =================================================================

import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
import urllib3

# Desativa os avisos de conexões HTTPS inseguras (devido ao verify=False)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURAÇÃO DE PASTA ---
ARQUIVO_NOME = "boletim5.html"

# CORRIGIDO: Nome da função ajustado de 'escribir_log' para 'escrever_log'
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
    # Lista com todos os 12 signos e seus respectivos nomes formatados para a URL do Terra
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
    
    # Define o signo do dia com base no dia do ano atual (muda todo dia à meia-noite)
    dia_do_ano = datetime.now().timetuple().tm_yday
    signo_hoje = signos[dia_do_ano % len(signos)]
    
    try:
        escrever_log(f"Buscando horóscopo do dia para {signo_hoje['nome']} (Terra)...")
        url = f"https://www.terra.com.br/vida-e-estilo/horoscopo/signos/{signo_hoje['slug']}/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        res = requests.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Coleta o parágrafo explicativo da previsão do dia no novo layout do Terra
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
        escrever_log("Buscando clima...")
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
            noticias.append(f"<li>{icone} {titulo} <a href='{link}'>[Leia mais]</a></li>")
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
    
    # Chama a função rotativa
    nome_signo, texto_signo = get_horoscopo_rotativo()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head><meta charset="UTF-8"><style>
        body {{ font-family: Arial; background: #f0f0f0; }}
        .container {{ max-width: 500px; background: #fff; margin: 10px auto; padding: 15px; border-radius: 5px; }}
        .section {{ margin-bottom: 10px; font-size: 14px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin-bottom: 6px; font-size: 13px; border-bottom: 1px dashed #eee; }}
    </style></head>
    <body>
        <div class="container">
            <div style="text-align:center">
                <p><i>"{get_frase_motivacional()}"</i></p>
                <b>*BOM DIA* | {agora.day}/{agora.month}</b>
            </div>
            <div class="section"><p>💵 Dólar R${d}<br>💶 Euro R${e}<br>📉 Ibov {i}</p></div>
            <div class="section"><p>🌡️ Máx {t_max}°C / Mín {t_min}°C | ☔ {chuva}%</p></div>
            <div class="section"><p>🔮 <b>{nome_signo}:</b> {texto_signo}</p></div>
            <div class="section"><ul>{noticias_br}</ul></div>
            <div class="section"><ul>{noticias_esporte}</ul></div>
        </div>
    </body>
    </html>"""
    
    with open(ARQUIVO_NOME, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    escrever_log(f"✅ Arquivo salvo com sucesso em: {os.path.abspath(ARQUIVO_NOME)}")

if __name__ == "__main__":
    gerar_boletim_html()