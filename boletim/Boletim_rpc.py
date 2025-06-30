import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup
from jinja2 import Template
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HG_WEATHER_KEY = "b2f3a461"

def dia_semana_pt():
    dias = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo"
    }
    return dias[datetime.now().weekday()]

def buscar_frase_motivacional():
    url = "https://www.frasesdobem.com.br/frases-aleatoria-do-dia/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    frase = soup.find("h2")
    return frase.text.strip() if frase else "Sorria: a vida retribui."

def buscar_comemoracoes():
    hoje = datetime.now()
    dia = hoje.day
    mes = hoje.strftime("%B").lower()
    url = f"https://www.calendarr.com/brasil/{mes}/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    comemoracoes = []
    for li in soup.find_all("li"):
        if f"{dia} de" in li.text[:15]:
            comemoracoes.append(li.text.split(" - ")[-1].strip())
    return ", ".join(comemoracoes) or "Sem comemorações registradas."

def buscar_clima():
    url = f"https://api.hgbrasil.com/weather?key={HG_WEATHER_KEY}&city_name=São Paulo"
    r = requests.get(url, verify=False).json()
    dados = r["results"]["forecast"][0]
    return {
        "descricao": dados["description"],
        "temp_max": dados["max"],
        "temp_min": dados["min"],
        "chuva": dados["rain"]
    }

def buscar_cambio():
    r = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL", verify=False).json()
    return {
        "dolar": f'R${float(r["USDBRL"]["bid"]):.2f}',
        "euro": f'R${float(r["EURBRL"]["bid"]):.2f}',
        "ibov": "136.865 (-0,18%)"
    }

def buscar_horoscopo():
    signos = {
        "aries": "Áries", "touro": "Touro", "gemeos": "Gêmeos", "cancer": "Câncer",
        "leao": "Leão", "virgem": "Virgem", "libra": "Libra", "escorpiao": "Escorpião",
        "sagitario": "Sagitário", "capricornio": "Capricórnio", "aquario": "Aquário", "peixes": "Peixes"
    }
    cod, nome = random.choice(list(signos.items()))
    url = f"https://joaobidu.com.br/horoscopo/signo/{cod}/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    p = soup.find("p")
    desc = p.text.strip() if p else "Hoje, siga a sua intuição. Você saberá o que fazer."
    return f"{nome}: {desc}"

def buscar_manchetes():
    g1 = [
        "Receita paga 2º lote do IR",
        "SP registra queda nos roubos",
        "Chuvas afetam safra de inverno"
    ]
    olhar = [
        "Brasil assume presidência do Mercosul",
        "MPF e SpaceX agem contra garimpo ilegal"
    ]
    return random.sample(g1 + olhar, 5)

def gerar_boletim():
    hoje = datetime.now()
    data = hoje.strftime("%d/%m/%Y")
    dia = dia_semana_pt()
    frase = buscar_frase_motivacional()
    comemoracoes = buscar_comemoracoes()
    clima = buscar_clima()
    cambio = buscar_cambio()
    horoscopo = buscar_horoscopo()
    noticias = buscar_manchetes()

    template = Template("""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Boletim Diário</title>
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
      <style>
        body {
          font-family: 'Inter', sans-serif;
          background: #f4f7fa;
          color: #333;
          max-width: 720px;
          margin: auto;
          padding: 2em;
        }
        h2 { color: #2c3e50; }
        section {
          background: #fff;
          border-radius: 8px;
          padding: 1.2em;
          margin-bottom: 20px;
          box-shadow: 0 0 8px rgba(0,0,0,0.03);
        }
        ul { padding-left: 1.2em; }
        li { margin-bottom: 0.5em; }
        .rodape {
          text-align: center;
          font-size: 0.8em;
          color: #999;
          margin-top: 2em;
        }
        .emoji {
          font-size: 1.4em;
          margin-right: 0.3em;
        }
      </style>
    </head>
    <body>
      <h2>☀️ Boletim Diário – {{ data }} ({{ dia }})</h2>

      <section>
        <p><span class="emoji">💬</span><em>{{ frase }}</em></p>
      </section>

      <section>
        <p><span class="emoji">🎉</span><strong>Comemorações:</strong> {{ comemoracoes }}</p>
      </section>

      <section>
        <p><span class="emoji">🌤</span><strong>Clima em São Paulo:</strong> {{ clima }} | Máx: {{ temp_max }}° | Mín: {{ temp_min }}° | Chuva: {{ chuva }}mm</p>
      </section>

      <section>
        <p><span class="emoji">💱</span><strong>Câmbio:</strong> Dólar: {{ dolar }} | Euro: {{ euro }} | Ibovespa: {{ ibov }}</p>
      </section>

      <section>
        <p><span class="emoji">🔮</span><strong>Horóscopo do dia:</strong> {{ horoscopo }}</p>
      </section>

      <section>
        <p><span class="emoji">📰</span><strong>Manchetes:</strong></p>
        <ul>{% for m in noticias %}<li>{{ m }}</li>{% endfor %}</ul>
      </section>

      <div class="rodape">© {{ hoje.year }} Reinaldo Pinheiro • Canal RPC – Dicas de Tecnologia</div>
    </body>
    </html>
    """)

    html = template.render(
        data=data,
        dia=dia,
        frase=frase,
        comemoracoes=comemoracoes,
        clima=clima["descricao"],
        temp_max=clima["temp_max"],
        temp_min=clima["temp_min"],
        chuva=clima["chuva"],
        dolar=cambio["dolar"],
        euro=cambio["euro"],
        ibov=cambio["ibov"],
        horoscopo=horoscopo,
        noticias=noticias,
        hoje=hoje
    )

    os.makedirs("boletim", exist_ok=True)
    with open("boletim/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Boletim gerado com sucesso: boletim/index.html")

# ▶️ Executar
gerar_boletim()
