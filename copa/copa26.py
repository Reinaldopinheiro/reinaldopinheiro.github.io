import os
from datetime import datetime

def gerar_html():
    # Coleta o horário atual de Brasília no formato: dd/mm/aaaa às hh:mm
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    status_texto = f"<strong>Status:</strong> Dados Oficiais Sincronizados. Última atualização: {agora}."

    # Define o caminho correto para ler o modelo HTML
    template_path = "copa_template.html"
    if not os.path.exists(template_path):
        template_path = os.path.join("copa", "copa_template.html")

    # Lê o arquivo HTML puríssimo
    with open(template_path, "r", encoding="utf-8") as f:
        html_puro = f.read()

    # Faz a substituição do placeholder pela string formatada
    html_final = html_puro.replace("__STATUS_BAR_PLACEHOLDER__", status_texto)

    # Escreve o arquivo final que o GitHub Pages vai renderizar
    with open("copa.html", "w", encoding="utf-8") as f:
        f.write(html_final)
        
    print(f"Sucesso! copa.html atualizado em {agora} com o bloco PIX no rodapé.")

if __name__ == "__main__":
    gerar_html()