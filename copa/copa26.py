import os
from string import Template

def buscar_dados_copa():
    # Dados limpos e isolados para o Python não se confundir com o JavaScript
    dados = {
        "A_1_P": 3, "A_2_P": 3, "B_1_P": 1, "C_1_P": 3, "C_2_P": 1
    }
    return dados

def gerar_html():
    dados = buscar_dados_copa()
    
    # HTML Base estruturado como Template pura (o Python ignora as chaves do CSS/JS)
    html_template = Template("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Central da Copa do Mundo 2026 - RPC Consultoria</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.2.3/css/flag-icons.min.css"/>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #f4f6f9; color: #1e293b; padding-bottom: 80px; }
        header { background: linear-gradient(135deg, #1e3a8a 25%, #0d9488 75%); color: white; padding: 35px 10px; text-align: center; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 15px; }
        .groups-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .group-card { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #0d9488; }
        .group-title { font-size: 15px; font-weight: bold; color: #1e3a8a; margin-bottom: 10px; text-transform: uppercase; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th { background-color: #1e3a8a; color: white; padding: 10px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
        .flag { display: inline-block; width: 20px; height: 15px; vertical-align: middle; margin-right: 6px; }
        footer { position: fixed; bottom: 0; left: 0; width: 100%; background: white; padding: 15px; text-align: center; font-weight: bold; border-top: 2px solid #e2e8f0; }
    </style>
</head>
<body>
    <header>
        <h1>Central da Copa do Mundo 2026 🏆</h1>
        <p>Tabela Completa de Grupos & Rodadas Atualizada</p>
    </header>

    <div class="container">
        <div class="groups-grid">
            <!-- GRUPO A -->
            <div class="group-card">
                <div class="group-title">Grupo A</div>
                <table>
                    <tr><th>Seleção</th><th>P</th><th>J</th></tr>
                    <tr><td><span class="flag fi fi-mx"></span> México</td><td><b>$A_1_P</b></td><td>1</td></tr>
                    <tr><td><span class="flag fi fi-kr"></span> Coreia do Sul</td><td><b>$A_2_P</b></td><td>1</td></tr>
                </table>
            </div>

            <!-- GRUPO C -->
            <div class="group-card">
                <div class="group-title">Grupo C</div>
                <table>
                    <tr><th>Seleção</th><th>P</th><th>J</th></tr>
                    <tr><td><span class="flag fi fi-gb-sct"></span> Escócia</td><td><b>$C_1_P</b></td><td>1</td></tr>
                    <tr><td><span class="flag fi fi-br"></span> BRASIL</td><td><b>$C_2_P</b></td><td>1</td></tr>
                </table>
            </div>
        </div>
    </div>

    <footer>Oferecimento: RPC - Reinaldo Pinheiro Consultoria</footer>
</body>
</html>""")

    # Preenche as variáveis com segurança utilizando o cifrão ($)
    html_final = html_template.safe_substitute(dados)

    with open("copa.html", "w", encoding="utf-8") as f:
        f.write(html_final)
    print("Arquivo copa.html gerado com sucesso!")

if __name__ == "__main__":
    gerar_html()