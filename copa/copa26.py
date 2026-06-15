import os
from datetime import datetime, timezone, timedelta

def gerar_html():
    # Cria o fuso horário GMT-3 (Horário de Brasília)
    fuso_brasilia = timezone(timedelta(hours=-3))
    
    # Coleta o horário atual já convertido para o GMT-3
    agora = datetime.now(fuso_brasilia).strftime("%d/%m/%Y às %H:%M")
    
    status_texto = f"<strong>Status:</strong> Dados Oficiais Sincronizados. Última atualização: {agora}."

    # Define o caminho correto para ler o modelo HTML.
    template_path = "copa_template.html"
    if not os.path.exists(template_path):
        template_path = os.path.join("copa", "copa_template.html")

    # Lê o arquivo HTML puríssimo
    with open(template_path, "r", encoding="utf-8") as f:
        html_puro = f.read()

    # Faz a substituição do placeholder pela string formatada com a hora certa
    html_final = html_puro.replace("__STATUS_BAR_PLACEHOLDER__", status_texto)

    # Escreve o arquivo final que o GitHub Pages vai renderizar
    with open("copa.html", "w", encoding="utf-8") as f:
        f.write(html_final)
        
    print(f"Sucesso! copa.html atualizado em {agora} (GMT-3).")

if __name__ == "__main__":
    gerar_html()