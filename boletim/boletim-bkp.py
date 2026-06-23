import requests
import random
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime
import yfinance as yf

# Caminhos
arquivo_excel = "C:\\Users\\reinaldo.pinheiro\\OneDrive\\Documents\\Programas_e_scripts\\boletim\\boletim_rpc.xlsx"
arquivo_frases = "C:\\Users\\reinaldo.pinheiro\\OneDrive\\Documents\\Programas_e_scripts\\boletim\\frases.rpc"
api_key = "7be2ec2d8d42047fb862869b55d75f83"

# Cria nova planilha
wb = Workbook()
ws = wb.active

# Cabeçalhos
ws.append([
    "Data", "Dólar (R$)", "Euro (R$)", "Ibovespa (pts)", "Ibovespa (%)",
    "Temp Máx (°C)", "Temp Mín (°C)", "Chuva (mm)", "Chuva (%)",
    "Horóscopo", "Notícia 1", "Notícia 2", "Notícia 3", "Notícia 4", "Notícia 5",
    "Frase Motivacional", "Notícia 6 (3I/ATLAS)", "Notícia 7 (Futebol)", "Notícia 8 (Futebol)", "Notícia 9 (Futebol)"
])

# Linha de dados
linha = [datetime.today().strftime("%d/%m/%Y")]

# Cotação
def get_cotacao_api(moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL"
    r = requests.get(url)
    try:
        valor = float(r.json()[f"{moeda}BRL"]["bid"])
        return round(valor, 2)
    except:
        return "Erro"

linha.append(get_cotacao_api("USD"))
linha.append(get_cotacao_api("EUR"))

# Ibovespa
def get_ibovespa():
    try:
        ibov = yf.Ticker("^BVSP")
        dados = ibov.history(period="2d")
        atual = round(dados["Close"].iloc[-1], 2)
        anterior = round(dados["Close"].iloc[-2], 2)
        variacao = round(((atual - anterior) / anterior) * 100, 2)
        return atual, f"{variacao:+.2f}%"
    except:
        return "Erro", "Erro"

ibov_valor, ibov_pct = get_ibovespa()
linha.extend([ibov_valor, ibov_pct])

# Tempo
def get_tempo(cidade="Sao Paulo", api_key=api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
        r = requests.get(url)
        dados = r.json()
        temp_max = round(dados["main"]["temp_max"], 1)
        temp_min = round(dados["main"]["temp_min"], 1)
        chuva_mm = round(dados.get("rain", {}).get("1h", 0), 1)
        descricao = dados["weather"][0]["description"]
        chuva_pct = 90 if "chuva" in descricao.lower() else 10
        return temp_max, temp_min, chuva_mm, f"{chuva_pct}%"
    except:
        return "Erro", "Erro", "Erro", "Erro"

linha.extend(get_tempo())

# Horóscopo
def get_horoscopo(signo="libra"):
    try:
        url = f"https://joaobidu.com.br/horoscopo/{signo}/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        texto = soup.find("div", class_="text-pred").text.strip()
        return f"{signo.capitalize()}: {texto}"
    except:
        return f"{signo.capitalize()}: Lua em Touro traz mudanças no trabalho e estabilidade emocional."

linha.append(get_horoscopo())

# Notícias gerais
def get_noticias_g1():
    try:
        url = "https://g1.globo.com/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        manchetes = soup.find_all("a", class_="feed-post-link", limit=5)
        return [m.text.strip() for m in manchetes]
    except:
        return ["Erro"] * 5

linha.extend(get_noticias_g1())

# Frase motivacional
def frase_motivacional(caminho=arquivo_frases):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            frases = [linha.strip() for linha in f if linha.strip()]
        return random.choice(frases)
    except:
        return "Tenha um ótimo dia!"

linha.append(frase_motivacional())

# Notícia 6 – 3I/ATLAS
def noticia_3i_atlas():
    try:
        url = "https://g1.globo.com/ciencia/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all("a", href=True)
        for link in links:
            if "atlas" in link["href"].lower() or "cometa" in link["href"].lower():
                return link.text.strip()
        return "Nenhuma notícia recente sobre o cometa 3I/ATLAS encontrada."
    except:
        return "Erro ao buscar notícia sobre 3I/ATLAS."

linha.append(noticia_3i_atlas())

# Notícias 7–9 – Futebol
def noticias_futebol():
    try:
        url = "https://ge.globo.com/futebol/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        manchetes = soup.find_all("a", class_="feed-post-link", limit=10)
        selecionadas = random.sample(manchetes, 3)
        return [m.text.strip() for m in selecionadas]
    except:
        return ["Erro"] * 3

linha.extend(noticias_futebol())

# Grava na planilha
ws.append(linha)
wb.save(arquivo_excel)
print("✅ Boletim atualizado com sucesso!")
