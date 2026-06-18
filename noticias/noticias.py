import requests
from bs4 import BeautifulSoup
import urllib3
import time
import os
from datetime import datetime
import tkinter as tk

# Supressão dos avisos de requisições inseguras
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Função para ler os links do arquivo texto
def read_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            links = f.readlines()
            links = [link.strip() for link in links if link.strip()]
        print(f"Links lidos do arquivo {file_path}: {links}")
        return links
    except Exception as e:
        print(f"Erro ao ler o arquivo de links: {e}")
        return []

# Função para obter manchetes com hiperlinks
def get_headlines(links):
    headlines_by_site = {}
    print("Obtendo manchetes...")

    for url in links:
        try:
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.content, 'xml')
            site_name = url.split('/')[2]  # Pega o nome do site do link
            news_items = soup.find_all('item', limit=5)
            headlines_by_site[site_name] = [(item.title.text, item.link.text) for item in news_items]
        except Exception as e:
            print(f"Erro ao obter manchetes do site {url}: {e}")

    return headlines_by_site

# Função para criar o arquivo HTML
def create_html():
    links = read_links('links.rpc')
    headlines_by_site = get_headlines(links)
    try:
        with open('noticias.html', 'w', encoding='utf-8') as f:
            f.write('<html><head><title>Noticias RPC</title><meta charset="UTF-8">\n')
            f.write('<meta http-equiv="refresh" content="60">\n')  # Meta tag para atualizar a cada 60 segundos
            f.write('</head><body>\n')
            f.write(f'<h1>Noticias RPC</h1>\n')

            for site, headlines in headlines_by_site.items():
                f.write(f'<h2>{site}</h2>\n<div class="noticias">\n')
                for headline, link in headlines:
                    f.write(f'<div class="noticia"><a href="{link}" target="_blank">{headline}</a></div>\n')
                f.write('</div>\n')

            f.write('</body></html>')

        print("Arquivo HTML criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar arquivo HTML: {e}")

# Função para adicionar a data da última atualização ao HTML
def add_last_update_date():
    src_path = 'noticias.html'
    try:
        last_update_time = os.path.getmtime(src_path)
        last_update_date = datetime.fromtimestamp(last_update_time).strftime('%d/%m/%Y %H:%M:%S')
        
        with open(src_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(content.replace('<h1>Noticias RPC</h1>', f'<h1>Noticias RPC</h1><p>Data da última atualização: {last_update_date}</p>', 1))
        
        print(f'Data da última atualização adicionada ao arquivo {src_path}.')
    except Exception as e:
        print(f"Erro ao adicionar data da última atualização ao arquivo: {e}")

# Função para atualizar a contagem regressiva na janela
def update_countdown(label, remaining):
    if remaining <= 0:
        label.config(text="Atualizando...")
        root.update()
        create_html()
        add_last_update_date()
        root.after(1000, start_countdown, label, 120)
    else:
        label.config(text=f"Próxima atualização em {remaining} segundos.")
        root.after(1000, update_countdown, label, remaining - 1)

# Função para iniciar a contagem regressiva
def start_countdown(label, remaining):
    update_countdown(label, remaining)

# Configuração da janela Tkinter
root = tk.Tk()
root.title("Noticias RPC")
root.geometry("340x150")  # Aumentei a largura da janela em mais 20 pixels

# Labels para o nome do programa e versão
title_label = tk.Label(root, text="Noticias RPC", font=("Helvetica", 16, "bold"))
title_label.pack(pady=5)

version_label = tk.Label(root, text="Versão: 4.1 - 31/01/2025", font=("Helvetica", 12))
version_label.pack(pady=5)

# Label para a contagem regressiva
countdown_label = tk.Label(root, text="", font=("Helvetica", 14))
countdown_label.pack(pady=10)

# Label para o copyright na parte inferior
copyright_label = tk.Label(root, text="© Reinaldo Pinheiro com Copilot", font=("Helvetica", 8))
copyright_label.pack(side="bottom", pady=5)

# Inicia a contagem regressiva
start_countdown(countdown_label, 120)

# Executa a janela Tkinter
root.mainloop()
