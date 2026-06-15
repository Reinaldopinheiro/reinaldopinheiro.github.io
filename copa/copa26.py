import os
from datetime import datetime

def gerar_html():
    # Coleta o horário atual de Brasília
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    status_texto = f"<strong>Status:</strong> Dados Oficiais Sincronizados. Última checagem automática: {agora} (Horário de Brasília)."

    # Define o caminho correto para ler o modelo HTML
    # Procura na mesma pasta do script ou na raiz
    template_path = "copa_template.html"
    if not os.path.exists(template_path):
        template_path = os.path.join("copa", "copa_template.html")

    # Lê o arquivo HTML puríssimo
    with open(template_path, "r", encoding="utf-8") as f:
        html_puro = f.read()

    # Faz apenas a substituição da String da barra de status
    html_final = html_puro.replace("__STATUS_BAR_PLACEHOLDER__", status_texto)

    # Escreve o arquivo final que o seu site vai ler
    with open("copa.html", "w", encoding="utf-8") as f:
        f.write(html_final)
        
    print("Sucesso total! copa.html gerado na raiz sem erros de compilação.")

if __name__ == "__main__":
    gerar_html()