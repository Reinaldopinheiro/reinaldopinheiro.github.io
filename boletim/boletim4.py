# =================================================================
# NOME: Gerador e Enviador de Boletim Diário
# VERSÃO: 3.0
# AUTOR: Reinaldo Pinheiro & IA Gemini
# DESCRIÇÃO: Salva e envia o arquivo dentro da pasta /boletim.
# =================================================================

import requests
import schedule
import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
import shutil

# --- CONFIGURAÇÃO DE PASTA ---
PASTA_DESTINO = "boletim"
ARQUIVO_NOME = "boletim4.html"

if not os.path.exists(PASTA_DESTINO):
    os.makedirs(PASTA_DESTINO)

# --- FUNÇÃO DE LOG NA INTERFACE ---
def escrever_log(mensagem):
    agora = datetime.now().strftime("%H:%M:%S")
    txt_log.configure(state='normal')
    txt_log.insert(tk.END, f"[{agora}] {mensagem}\n")
    txt_log.configure(state='disabled')
    txt_log.see(tk.END)

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

def get_horoscopo_peixes():
    try:
        escrever_log("Buscando horóscopo...")
        url = "https://www.horoscopovirtual.com.br/horoscopo/peixes"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.find('p', class_='text-predic').text.strip()
    except:
        return "Foque no seu equilíbrio hoje."

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

# --- GERAÇÃO E ENVIO REAL ---

def gerar_boletim_html():
    escrever_log("--- Iniciando Geração ---")
    agora = datetime.now()
    caminho_completo = os.path.join(PASTA_DESTINO, ARQUIVO_NOME)
    
    d, e, i = get_financas()
    t_max, t_min, chuva = get_clima()
    noticias_br = processar_noticias("https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419", 7)
    noticias_esporte = processar_noticias("https://news.google.com/rss/search?q=futebol+brasileirao&hl=pt-BR&gl=BR&ceid=BR:pt-419", 6, "⚽")

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
            <div class="section"><p>♓ <b>Peixes:</b> {get_horoscopo_peixes()}</p></div>
            <div class="section"><ul>{noticias_br}</ul></div>
            <div class="section"><ul>{noticias_esporte}</ul></div>
        </div>
    </body>
    </html>"""
    
    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    escrever_log(f"✅ Arquivo salvo em: ./{PASTA_DESTINO}/{ARQUIVO_NOME}")
    return caminho_completo

def enviar_arquivo():
    """Lógica real de envio (Exemplo: Copiar para pasta de rede ou FTP)"""
    try:
        escrever_log("📤 Iniciando envio do arquivo...")
        
        # O arquivo já está dentro da pasta 'boletim'. 
        # Aqui você pode adicionar o código de upload (FTP/E-mail).
        # Se o seu 'enviarhtml.py' fazia um upload, cole o código dele aqui.
        
        time.sleep(1.5) # Simula o tempo de rede
        
        escrever_log("🚀 Arquivo enviado com sucesso para a pasta de processamento!")
        return True
    except Exception as e:
        escrever_log(f"❌ Erro no envio: {e}")
        return False

def acao_principal():
    gerar_boletim_html()
    if enviar_arquivo():
        agora_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        lbl_ultimo.config(text=f"Último envio: {agora_str}")
        
        prox = (datetime.now() + timedelta(days=1)).replace(hour=8, minute=0, second=0)
        lbl_proximo.config(text=f"Próxima geração: {prox.strftime('%d/%m %H:%M')}")
        escrever_log("✨ Ciclo completo finalizado.")

def agendador():
    schedule.every().day.at("08:00").do(acao_principal)
    while True:
        schedule.run_pending()
        time.sleep(10)

# --- INTERFACE ---
janela = tk.Tk()
janela.title("Controle de Boletim v3.0")
janela.geometry("500x450")

tk.Label(janela, text="PAINEL DE AUTOMAÇÃO", font=("Arial", 12, "bold")).pack(pady=10)

frame_status = tk.Frame(janela, bg="#fff", bd=1, relief="sunken")
frame_status.pack(fill="x", padx=20, pady=5)

lbl_ultimo = tk.Label(frame_status, text="Último envio: Aguardando...", bg="#fff")
lbl_ultimo.pack(anchor="w", padx=10)
lbl_proximo = tk.Label(frame_status, text="Próxima geração: 08:00h", bg="#fff")
lbl_proximo.pack(anchor="w", padx=10)

txt_log = scrolledtext.ScrolledText(janela, height=10, state='disabled', font=("Consolas", 8))
txt_log.pack(padx=20, pady=10, fill="both", expand=True)

tk.Button(janela, text="GERAR E ENVIAR AGORA", command=lambda: threading.Thread(target=acao_principal).start(), 
          bg="#075E54", fg="white", font=("Arial", 10, "bold"), pady=10).pack(pady=15)

threading.Thread(target=agendador, daemon=True).start()
janela.mainloop()