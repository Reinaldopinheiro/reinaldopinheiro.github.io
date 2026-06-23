# boletim3.py - Versão 4.4
# Última Atualização: 02/02/2026 11:10 (Horário de Brasília)
# Criado por Reinaldo de Almeida Pinheiro em Python e A.I. Gemini

import os
import requests
import random
import pywhatkit
import yfinance as yf
import re
import time
import urllib3
from datetime import datetime
from bs4 import BeautifulSoup

# Configurações de ambiente para evitar erros de rede/SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['PYWHATKIT_SKIP_INTERNET_CHECK'] = 'True'

# === CONFIGURAÇÕES DE ARQUIVOS ===
arquivo_sequencia = "Sequencia.rpc"
arquivo_envios = "envia.rpc"
arquivo_frases = "frases.rpc"
api_key = "7be2ec2d8d42047fb862869b55d75f83"
agora = datetime.now()

# 1. Controle de Sequência
def carregar_sequencia():
    ano_atual = agora.year % 100
    if os.path.exists(arquivo_sequencia):
        with open(arquivo_sequencia, "r", encoding="utf-8") as f:
            linha = f.read().strip()
            try:
                numero, ano = linha.split("/")
                if int(ano) == ano_atual:
                    return int(numero), ano_atual
            except: pass
    return 1, ano_atual

num_bol, ano_bol = carregar_sequencia()
numero_formatado = f"{num_bol:04d}/{ano_bol}"

# 2. Coleta de Informações (Frase, Saudação e Data)
def get_frase():
    if os.path.exists(arquivo_frases):
        with open(arquivo_frases, "r", encoding="utf-8") as f:
            frases = [l.strip() for l in f if l.strip()]
            return random.choice(frases)
    return "A persistência realiza o impossível."

saudacao = "BOM DIA!" if agora.hour < 12 else "BOA TARDE!" if agora.hour < 18 else "BOA NOITE!"
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
dia_fig = "".join([f"{n}️⃣" for n in agora.strftime("%d")])
data_extenso = f"{dia_fig} de {meses[agora.month-1]}"
dia_semana_txt = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"][agora.weekday()]

# 3. Funções de Scraping e Economia
def get_cotacao(moeda):
    try:
        r = requests.get(f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL", verify=False, timeout=10).json()
        return f"{float(r[f'{moeda}BRL']['bid']):.2f}"
    except: return "Erro"

def get_ibovespa():
    try:
        # Busca dados do Yahoo Finance para o ticker ^BVSP (Ibovespa)
        ibov = yf.Ticker("^BVSP")
        dados = ibov.history(period="5d") # Pega 5 dias para garantir dados de fechamento
        if not dados.empty:
            atual = round(dados["Close"].iloc[-1], 2)
            anterior = round(dados["Close"].iloc[-2], 2)
            variacao = round(((atual - anterior) / anterior) * 100, 2)
            return f"{int(atual):,} pts".replace(",", "."), f"{variacao:+.2f}%"
    except Exception as e:
        print(f"Erro Ibovespa: {e}")
    return "Indisponível", "0.00%"

ibov_valor, ibov_var = get_ibovespa()

def get_horoscopo():
    signos = ["aries", "touro", "gemeos", "cancer", "leao", "virgem", "libra", "escorpiao", "sagitario", "capricornio", "aquario", "peixes"]
    s = random.choice(signos)
    try:
        r = requests.get(f"https://www.uol.com.br/universa/horoscopo/{s}/horoscopo-do-dia/", verify=False, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        texto = soup.find('p', class_='text').get_text()[:150]
        return s.capitalize(), f"{texto}..."
    except: return s.capitalize(), "O dia pede foco e equilíbrio nos objetivos."

def get_noticias_limpas(url, limite, icone):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        # Seleciona manchetes baseadas nas classes comuns da Globo/GE
        tags = soup.find_all(['a', 'h2'], class_=re.compile("feed-post-link|content-head__title"), limit=limite)
        return [f"{icone} {t.get_text().strip()}" for t in tags]
    except: return []

# === MONTAGEM DO CORPO DO BOLETIM (SEM TRAÇOS) ===
noticias_lista = []
noticias_lista.extend(get_noticias_limpas("https://g1.globo.com/politica/", 2, "🔹"))
noticias_lista.extend(get_noticias_limpas("https://g1.globo.com/economia/", 2, "🔸"))
noticias_lista.extend(get_noticias_limpas("https://g1.globo.com/sp/sao-paulo/", 2, "🏢"))
noticias_lista.extend(get_noticias_limpas("https://ge.globo.com/futebol/", 3, "⚽"))

corpo_noticias = "\n".join(noticias_lista)

boletim_texto = f"""Boletim Diário RPC - {numero_formatado}

📝 {get_frase()}

**{saudacao}**
{data_extenso}
**{dia_semana_txt}**

💰 ECONOMIA
• Dólar: R$ {get_cotacao("USD")}
• Euro: R$ {get_cotacao("EUR")}
• Ibovespa: {ibov_valor} ({ibov_var})

🔮 SIGNO: {get_horoscopo()[0]}
✨ {get_horoscopo()[1]}

{corpo_noticias}

© RPC Reinaldo Pinheiro Consultoria
📚 Leia o livro: http://reinaldopinheiro.com.br/livro.html
💰 Pix: doe@reinaldopinheiro.com.br"""

# === ROTINA DE ENVIO INTEGRADA DO BOLETIM2.PY ===
try:
    if os.path.exists(arquivo_envios):
        with open(arquivo_envios, "r", encoding="utf-8") as f:
            linhas_envio = [l.strip() for l in f if l.strip()]
        
        tempo_espera = int(linhas_envio[0])
        numeros = linhas_envio[1:]

        if tempo_espera == 999:
            print("⏸️ Envio via WhatsApp desativado (999 encontrado)")
        else:
            if tempo_espera > 0:
                print(f"⏳ Aguardando {tempo_espera} unidades de tempo...")
                time.sleep(tempo_espera)
            
            for numero in numeros:
                pywhatkit.sendwhatmsg_instantly(numero, boletim_texto, wait_time=20, tab_close=True)
                print(f"✅ Boletim enviado para {numero}")
                
        # Atualiza sequência
        with open(arquivo_sequencia, "w", encoding="utf-8") as f:
            f.write(f"{num_bol + 1:04d}/{ano_bol}")

except Exception as e:
    print(f"❌ Erro no envio: {e}")

# === GERAÇÃO DO HTML (ESTILO WHATSAPP COM FUNDO VERDE) ===
html_final = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
    body {{ background-color: #0b141a; display: flex; justify-content: center; padding: 20px; font-family: 'Segoe UI', sans-serif; }}
    .balao {{ 
        background-color: #d9fdd3; 
        padding: 18px; 
        border-radius: 10px; 
        max-width: 550px; 
        white-space: pre-wrap; 
        line-height: 1.5; 
        font-size: 15px; 
        color: #111b21; 
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }}
</style></head>
<body><div class="balao">{boletim_texto}</div></body></html>"""

with open("boletim.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print(boletim_texto)
print("\n*** Fim do Programa ***")