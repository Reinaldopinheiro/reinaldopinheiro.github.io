import requests
from bs4 import BeautifulSoup
import urllib3
import os
from datetime import datetime, timedelta, timezone

# ==============================================================================
# PROGRAMA: NOTICIAS RPC
# VERSÃO: 5.4
# DATA DA VERSÃO: 18/06/2026
# DESENVOLVEDORES: Reinaldo Pinheiro Consultoria com Gemini
# DESCRIÇÃO: Fuso GMT-3 corrigido + Auto-refresh HTML a cada 2 minutos.
# ==============================================================================

# Supressão dos avisos de requisições inseguras
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def get_headlines(links):
    headlines_by_site = {}
    print("Obtendo manchetes...")

    for url in links:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, verify=False, timeout=15)
            soup = BeautifulSoup(response.content, 'xml')
            site_name = url.split('/')[2]
            news_items = soup.find_all('item', limit=5)
            headlines_by_site[site_name] = [(item.title.text, item.link.text) for item in news_items]
        except Exception as e:
            print(f"Erro ao obter manchetes do site {url}: {e}")

    return headlines_by_site

def create_html():
    links = read_links('links.rpc')
    headlines_by_site = get_headlines(links)
    
    # Fuso Horário de Brasília (GMT-3)
    fuso_brasilia = timezone(timedelta(hours=-3))
    gmt_minus_3 = datetime.now(fuso_brasilia)
    last_update_date = gmt_minus_3.strftime('%d/%m/%Y %H:%M:%S')
    
    pix_key = "doe@reinaldopinheiro.com.br"
    qrcode_filename = "noticias-qrcode-pix.png"

    try:
        with open('noticias.html', 'w', encoding='utf-8') as f:
            f.write('<html><head><title>NOTICIAS RPC</title><meta charset="UTF-8">\n')
            
            # --- ADICIONADO AQUI: Recarrega a página no navegador do usuário a cada 120 segundos (2 minutos) ---
            f.write('<meta http-equiv="refresh" content="120">\n')
            
            f.write('<style>\n')
            f.write('  body { font-family: Helvetica, Arial, sans-serif; margin: 40px; color: #333; background-color: #f9f9f9; }\n')
            f.write('  h1 { color: #111; border-bottom: 2px solid #333; padding-bottom: 10px; }\n')
            f.write('  h2 { color: #0056b3; margin-top: 30px; }\n')
            f.write('  .noticia { margin: 10px 0; padding: 5px; }\n')
            f.write('  .noticia a { text-decoration: none; color: #222; font-size: 16px; }\n')
            f.write('  .noticia a:hover { color: #0056b3; text-decoration: underline; }\n')
            f.write('  footer { margin-top: 50px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 13px; color: #555; text-align: center; }\n')
            f.write('  .donate-box { display: inline-block; text-align: center; margin-top: 15px; padding: 10px; border: 1px dashed #28a745; background-color: #f1fbf3; border-radius: 5px; }\n')
            f.write('  .donate-box img { margin-top: 8px; max-width: 150px; height: auto; }\n')
            f.write('</style>\n')
            f.write('</head><body>\n')
            
            f.write('<h1>NOTICIAS RPC</h1>\n')
            f.write(f'<p><em>Data da última atualização: {last_update_date}</em></p>\n')

            for site, headlines in headlines_by_site.items():
                f.write(f'<h2>{site}</h2>\n<div class="noticias">\n')
                for headline, link in headlines:
                    f.write(f'<div class="noticia"><a href="{link}" target="_blank">{headline}</a></div>\n')
                f.write('</div>\n')

            f.write('<footer>\n')
            f.write('  <p>© 2026 Copyright Reinaldo Pinheiro Consultoria com Gemini - Versão 5.4 (Script Automático)</p>\n')
            f.write('  <div class="donate-box">\n')
            f.write(f'    <strong>🎁 Ajude a criar novos projetos</strong><br>\n')
            f.write(f'    Chave PIX: <code>{pix_key}</code><br>\n')
            f.write(f'    <img src="{qrcode_filename}" alt="QRCode PIX Donate" title="Escaneie para doar"><br>\n')
            f.write('    <span>Aponte a câmera do seu banco para o QRCode</span>\n')
            f.write('  </div>\n')
            f.write('</footer>\n')

            f.write('</body></html>')

        print("Arquivo HTML criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar arquivo HTML: {e}")

if __name__ == "__main__":
    create_html()