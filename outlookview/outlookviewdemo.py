# ================================================================================
# NOME DO PROGRAMA: Outlook Calendar Analytics (DEMO)
# VERSÃO: 1.3.0-DEMO (Logo, Suporte PIX e QR Code)
# DATA DE ATUALIZAÇÃO: 03 de Agosto de 2026
# COPYRIGHT: Reinaldo Pinheiro 2026
# ================================================================================

import os
import sys
import re
import random
import webbrowser
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    import pandas as pd
    import plotly.express as px
    from PIL import Image, ImageTk
except ImportError as e:
    print(f"Erro ao importar bibliotecas: {e}")
    print("Execute: pip install pandas plotly pillow")

# --------------------------------------------------------------------------------
# CONSTANTES DE IDENTIFICAÇÃO DO SISTEMA
# --------------------------------------------------------------------------------
PROGRAM_NAME = "Outlook Calendar Analytics [DEMO]"
PROGRAM_VERSION = "v1.3.0-DEMO"
PROGRAM_DATE = "03/08/2026"
COPYRIGHT_TEXT = "Copyright © Reinaldo Pinheiro 2026. Todos os direitos reservados."
PIX_MSG = "Ajude a criar mais projetos como esse, colabore! Pix: doe@reinaldopinheiro.com.br"

class OutlookAnalyticsAppDemo:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{PROGRAM_NAME} - {PROGRAM_VERSION}")
        self.root.geometry("640x700")
        self.root.resizable(False, False)
        
        self.data_inicio = "01/01/2026"
        self.data_fim = datetime.datetime.now().strftime("%d/%m/%Y")
        self.ultimo_html_gerado = None
        self.nome_conta_outlook = "demo.usuario@empresa.com.br (Fictícia)"

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.bg_color = "#f4f6f9"
        self.primary_color = "#2b6cb0"
        
        self.root.configure(bg=self.bg_color)
        
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=self.primary_color, background=self.bg_color)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9, "italic"), foreground="#64748b", background=self.bg_color)
        self.style.configure("Info.TLabel", font=("Segoe UI", 10), foreground="#334155", background=self.bg_color)
        self.style.configure("Copyright.TLabel", font=("Segoe UI", 8, "bold"), foreground="#475569", background="#e2e8f0")
        
        self.style.configure("Main.TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def create_widgets(self):
        header_frame = ttk.Frame(self.root, padding="10 10 10 5")
        header_frame.pack(fill=tk.X)
        
        # Carregar Logo na Interface se existir
        if os.path.exists("logo.png"):
            try:
                img_logo = Image.open("logo.png")
                img_logo.thumbnail((180, 50))
                self.logo_tk = ImageTk.PhotoImage(img_logo)
                lbl_logo_img = ttk.Label(header_frame, image=self.logo_tk, background=self.bg_color)
                lbl_logo_img.pack(anchor=tk.CENTER, pady=(0, 5))
            except Exception:
                pass

        ttk.Label(header_frame, text=PROGRAM_NAME, style="Header.TLabel").pack(anchor=tk.CENTER)
        
        info_version_text = f"Versão: {PROGRAM_VERSION}  |  Data de Atualização: {PROGRAM_DATE}"
        ttk.Label(header_frame, text=info_version_text, style="SubHeader.TLabel").pack(anchor=tk.CENTER, pady=(2, 5))

        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15)

        status_frame = ttk.Frame(self.root, padding="15 10 15 10")
        status_frame.pack(fill=tk.X)

        self.lbl_periodo = ttk.Label(
            status_frame, 
            text=f"📅 Período Selecionado: {self.data_inicio} até {self.data_fim}", 
            style="Info.TLabel",
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_periodo.pack(anchor=tk.CENTER, pady=3)

        config_frame = ttk.Frame(status_frame)
        config_frame.pack(anchor=tk.CENTER, pady=5)
        
        ttk.Label(config_frame, text="📊 Agrupar por:", style="Info.TLabel").pack(side=tk.LEFT, padx=3)
        self.combo_gran = ttk.Combobox(config_frame, values=["Ano", "Mês", "Dia"], state="readonly", width=8)
        self.combo_gran.set("Mês")
        self.combo_gran.pack(side=tk.LEFT, padx=5)

        ttk.Label(config_frame, text="📈 Principais Ocorrências:", style="Info.TLabel").pack(side=tk.LEFT, padx=(10, 3))
        self.combo_grafico = ttk.Combobox(config_frame, values=["Pizza", "Barras"], state="readonly", width=8)
        self.combo_grafico.set("Pizza")
        self.combo_grafico.pack(side=tk.LEFT, padx=5)

        self.lbl_status = ttk.Label(
            status_frame, 
            text="Modo de Demonstração: Dados gerados sinteticamente.", 
            style="SubHeader.TLabel"
        )
        self.lbl_status.pack(anchor=tk.CENTER, pady=2)

        btn_container = ttk.Frame(self.root, padding="20 5 20 10")
        btn_container.pack(fill=tk.BOTH, expand=True)

        self.btn_pedir_periodo = ttk.Button(
            btn_container, 
            text="📅 Pedir Período (Ex: 2026)", 
            style="Main.TButton",
            command=self.acao_pedir_periodo
        )
        self.btn_pedir_periodo.pack(fill=tk.X, pady=4)

        self.btn_colocar_periodo = ttk.Button(
            btn_container, 
            text="✏️ Colocar Período Personalizado (Início e Fim)", 
            style="Main.TButton",
            command=self.acao_colocar_periodo
        )
        self.btn_colocar_periodo.pack(fill=tk.X, pady=4)

        self.btn_nova_consulta = ttk.Button(
            btn_container, 
            text="🌐 Gerar Relatório HTML (Demonstração)", 
            style="Main.TButton",
            command=self.acao_gerar_consulta
        )
        self.btn_nova_consulta.pack(fill=tk.X, pady=4)

        self.btn_ver_html = ttk.Button(
            btn_container, 
            text="💻 Ver o HTML Gerado no Navegador", 
            style="Main.TButton",
            command=self.acao_ver_html
        )
        self.btn_ver_html.pack(fill=tk.X, pady=4)

        self.btn_sair = ttk.Button(
            btn_container, 
            text="❌ Sair", 
            style="Main.TButton",
            command=self.root.quit
        )
        self.btn_sair.pack(fill=tk.X, pady=4)

        footer_frame = tk.Frame(self.root, bg="#e2e8f0", height=45)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        lbl_pix = ttk.Label(footer_frame, text=PIX_MSG, style="Copyright.TLabel")
        lbl_pix.pack(anchor=tk.CENTER, pady=(6, 1))

        lbl_copy = ttk.Label(footer_frame, text=COPYRIGHT_TEXT, style="Copyright.TLabel", font=("Segoe UI", 7))
        lbl_copy.pack(anchor=tk.CENTER, pady=(0, 6))

    def acao_pedir_periodo(self):
        ano = simpledialog.askstring("Pedir Período", "Digite o ano para análise (ex: 2026):", parent=self.root)
        if ano and ano.isdigit() and len(ano) == 4:
            self.data_inicio = f"01/01/{ano}"
            hoje = datetime.datetime.now()
            if int(ano) == hoje.year:
                self.data_fim = hoje.strftime("%d/%m/%Y")
            else:
                self.data_fim = f"31/12/{ano}"

            self.lbl_periodo.config(text=f"📅 Período Selecionado: {self.data_inicio} até {self.data_fim}")
            self.lbl_status.config(text=f"Ano {ano} configurado.")
        elif ano:
            messagebox.showerror("Ano Inválido", "Por favor, informe um ano com 4 dígitos (ex: 2026).")

    def acao_colocar_periodo(self):
        dt_ini = simpledialog.askstring("Colocar Período", "Data Inicial (DD/MM/AAAA):", initialvalue=self.data_inicio, parent=self.root)
        if not dt_ini:
            return
        dt_fim = simpledialog.askstring("Colocar Período", "Data Final (DD/MM/AAAA):", initialvalue=self.data_fim, parent=self.root)
        if not dt_fim:
            return
        
        self.data_inicio = dt_ini
        self.data_fim = dt_fim
        self.lbl_periodo.config(text=f"📅 Período Selecionado: {self.data_inicio} até {self.data_fim}")

    def acao_ver_html(self):
        if self.ultimo_html_gerado and os.path.exists(self.ultimo_html_gerado):
            webbrowser.open(os.path.abspath(self.ultimo_html_gerado))
        else:
            messagebox.showwarning("Aviso", "Nenhum relatório HTML foi gerado ainda.")

    def acao_gerar_consulta(self):
        self.lbl_status.config(text="Gerando base de dados fictícia...")
        self.root.update()

        try:
            df_eventos = self.gerar_dados_ficticios()
            if df_eventos is None or df_eventos.empty:
                messagebox.showwarning("Sem Resultados", "Nenhum dado fictício gerado no período.")
                return

            granularidade = self.combo_gran.get()
            tipo_grafico = self.combo_grafico.get()
            
            html_file = self.gerar_dashboard_html(df_eventos, granularidade, tipo_grafico)
            self.ultimo_html_gerado = html_file

            self.lbl_status.config(text=f"✅ Relatório DEMO gerado com sucesso!")
            
            resp = messagebox.askyesno("Demonstração Gerada", f"Dashboard de demonstração gerado!\nAgrupamento: {granularidade}\nGráfico: {tipo_grafico}\n\nDeseja abrir o relatório HTML agora?")
            if resp:
                self.acao_ver_html()

        except Exception as e:
            messagebox.showerror("Erro de Demonstração", f"Erro ao gerar dados:\n{str(e)}")
            self.lbl_status.config(text="Erro de execução.")

    def gerar_dados_ficticios(self):
        dt_inicio_obj = datetime.datetime.strptime(f"{self.data_inicio}", "%d/%m/%Y")
        dt_fim_obj = datetime.datetime.strptime(f"{self.data_fim}", "%d/%m/%Y")
        
        dias_totais = (dt_fim_obj - dt_inicio_obj).days
        if dias_totais <= 0:
            dias_totais = 1

        pessoas = ["Carlos Silva", "Ana Souza", "Mariana Oliveira", "Roberto Lima", "Fernanda Santos", "Lucas Mendes"]
        organizadores = ["gerente@empresa.com", "ti@empresa.com", "coord.operacoes@empresa.com", "suporte@empresa.com"]
        
        assuntos_pool = [
            ("Suporte Carlos - Troca de Senha", "Suporte Técnico", "Troca De Senha"),
            ("Suporte Ana - Erro no VPN", "Suporte Técnico", "Erro Vpn"),
            ("Suporte Mariana - Configurar E-mail", "Suporte Técnico", "Configurar E-Mail"),
            ("Suporte Roberto - Lento o Sistema", "Suporte Técnico", "Lentidão"),
            ("Reunião Semanal de Alinhamento", "Reuniões Internas", "Outros"),
            ("Sync de Alinhamento T.I", "Reuniões Internas", "Outros"),
            ("Compromisso pessoal médico", "Outros Atendimentos", "Outros"),
            ("Atendimento Pessoal RH", "Outros Atendimentos", "Outros"),
            ("Ajuste de Impressora", "Suporte Técnico", "Impressora"),
            ("Instalação de Software", "Suporte Técnico", "Instalação")
        ]

        records = []
        qtd_eventos = min(max(dias_totais * 3, 20), 300)

        for _ in range(qtd_eventos):
            dias_rand = random.randint(0, dias_totais)
            data_evento = dt_inicio_obj + datetime.timedelta(days=dias_rand, hours=random.randint(8, 17), minutes=random.choice([0, 15, 30, 45]))
            
            assunto, categoria, grupo = random.choice(assuntos_pool)
            duracao = random.choice([0.5, 1.0, 1.5, 2.0])
            
            text_lower = assunto.lower()

            if "pessoal" in text_lower:
                continue

            pessoa_atendida = random.choice(pessoas) if categoria == "Suporte Técnico" else random.choice(organizadores)

            records.append({
                "Assunto": assunto,
                "Inicio": data_evento.strftime("%Y-%m-%d %H:%M"),
                "Ano": data_evento.strftime("%Y"),
                "Mes_Ano": data_evento.strftime("%Y-%m"),
                "Dia_Mes_Ano": data_evento.strftime("%Y-%m-%d"),
                "Duracao_Horas": duracao,
                "Organizador": random.choice(organizadores),
                "Pessoa_Atendida": pessoa_atendida,
                "Categoria": categoria,
                "Grupo_Agrupar": grupo
            })

        return pd.DataFrame(records)

    def gerar_dashboard_html(self, df, granularidade="Mês", tipo_grafico="Pizza"):
        coluna_tempo = "Mes_Ano"
        titulo_tempo = "Mensal"
        if granularidade == "Ano":
            coluna_tempo = "Ano"
            titulo_tempo = "Anual"
        elif granularidade == "Dia":
            coluna_tempo = "Dia_Mes_Ano"
            titulo_tempo = "Diária"

        df_agrupar = df[df['Grupo_Agrupar'] != "Outros"]
        if df_agrupar.empty:
            df_agrupar = df

        df_agrupar_summary = df_agrupar.groupby('Grupo_Agrupar').agg(
            Qtd_Ocorrencias=('Assunto', 'count'),
            Total_Horas=('Duracao_Horas', 'sum')
        ).reset_index()

        total_horas_agrupar = df_agrupar_summary['Total_Horas'].sum()
        df_agrupar_summary['Porcentagem'] = (df_agrupar_summary['Total_Horas'] / total_horas_agrupar * 100).round(1)

        df_agrupar_summary['Rotulo_Legenda'] = df_agrupar_summary.apply(
            lambda r: f"{r['Grupo_Agrupar']} ({r['Qtd_Ocorrencias']}x)", axis=1
        )

        if tipo_grafico == "Barras":
            df_agrupar_summary = df_agrupar_summary.sort_values(by='Total_Horas', ascending=True)
            fig_principais = px.bar(
                df_agrupar_summary,
                x='Porcentagem',
                y='Rotulo_Legenda',
                orientation='h',
                text=df_agrupar_summary['Porcentagem'].apply(lambda v: f"{v}%"),
                title='<b>Principais Ocorrências (% de Atendimento)</b>',
                labels={'Porcentagem': 'Porcentagem (%)', 'Rotulo_Legenda': 'Ocorrência (Qtd)'},
                color_discrete_sequence=['#2b6cb0']
            )
            fig_principais.update_traces(
                textposition='outside',
                hovertemplate="<b>%{y}</b><br>Horas Totais: %{customdata:.1f}h<br>Porcentagem: %{x}%",
                customdata=df_agrupar_summary['Total_Horas']
            )
        else:
            fig_principais = px.pie(
                df_agrupar_summary, 
                names='Rotulo_Legenda', 
                values='Total_Horas',
                title='<b>Principais Ocorrências (% de Atendimento)</b>', 
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_principais.update_traces(
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Horas Totais: %{value:.1f}h<br>Porcentagem: %{percent}"
            )

        fig_principais.update_layout(font=dict(family="Segoe UI, sans-serif"))

        fig_cat = px.pie(
            df, names='Categoria', values='Duracao_Horas',
            title='<b>Distribuição de Horas por Categoria</b>', hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_cat.update_layout(font=dict(family="Segoe UI, sans-serif"))

        df_tempo = df.groupby([coluna_tempo, 'Categoria'])['Duracao_Horas'].sum().reset_index()
        fig_tempo = px.bar(
            df_tempo, x=coluna_tempo, y='Duracao_Horas', color='Categoria',
            title=f'<b>Evolução {titulo_tempo} de Horas</b>', barmode='stack',
            labels={coluna_tempo: f"Período ({granularidade})", "Duracao_Horas": "Horas Totais"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_tempo.update_layout(font=dict(family="Segoe UI, sans-serif"))

        df_suporte = df[df['Categoria'] == 'Suporte Técnico'].copy()
        df_outros = df[df['Categoria'] != 'Suporte Técnico'].copy()

        tb_suporte_pessoa = df_suporte.groupby('Pessoa_Atendida').agg(
            Qtd_Suportes=('Assunto', 'count'),
            Total_Horas=('Duracao_Horas', 'sum')
        ).reset_index().sort_values(by='Qtd_Suportes', ascending=False)

        rows_suporte_pessoa = ""
        for _, r in tb_suporte_pessoa.iterrows():
            rows_suporte_pessoa += f"<tr><td><b>{r['Pessoa_Atendida']}</b></td><td>{r['Qtd_Suportes']} atendimentos</td><td>{round(r['Total_Horas'], 1)}h</td></tr>"

        df_outros_resumo = df_outros.groupby(['Assunto', 'Organizador']).agg(
            Qtd=('Categoria', 'count'),
            Total_Horas=('Duracao_Horas', 'sum')
        ).reset_index().sort_values(by=['Qtd', 'Total_Horas'], ascending=False).head(50)

        rows_outros_resumo = ""
        for _, r in df_outros_resumo.iterrows():
            rows_outros_resumo += f"<tr><td>{r['Assunto']}</td><td>{r['Organizador']}</td><td>{r['Qtd']}</td><td>{round(r['Total_Horas'], 1)}h</td></tr>"

        rows_lista_suporte = ""
        for _, r in df_suporte.sort_values(by='Inicio', ascending=False).iterrows():
            rows_lista_suporte += f"<tr><td>{r['Inicio']}</td><td><b>{r['Pessoa_Atendida']}</b></td><td>{r['Assunto']}</td><td>{r['Duracao_Horas']}h</td></tr>"

        total_horas = round(df['Duracao_Horas'].sum(), 1)
        total_eventos = len(df)
        total_suportes = len(df_suporte)

        # IMAGENS NO HTML (LOGO E QRCODE)
        html_logo_tag = '<img src="logo.png" alt="Logo" style="max-height: 60px; margin-bottom: 15px;">' if os.path.exists("logo.png") else ''
        html_qrcode_tag = '<div style="margin-top: 12px;"><img src="QRCODE.png" alt="QR Code Pix" style="width: 110px; height: 110px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.15);"></div>' if os.path.exists("QRCODE.png") else ''

        html_code = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório DEMO - {PROGRAM_NAME}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 20px; }}
        .header-card {{ background: linear-gradient(135deg, #2b6cb0, #1a365d); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 25px; text-align: center; }}
        .header-card h1 {{ margin: 0 0 10px 0; font-size: 24px; }}
        .params-box {{ background: rgba(255, 255, 255, 0.15); border-left: 4px solid #63b3ed; padding: 12px 18px; border-radius: 6px; margin-top: 15px; font-size: 14px; line-height: 1.6; text-align: left; }}
        .account-badge {{ display: inline-block; background: rgba(255,255,255,0.25); padding: 4px 12px; border-radius: 20px; font-weight: bold; margin-top: 10px; font-size: 13px; }}
        .kpi-row {{ display: flex; gap: 15px; margin-bottom: 25px; }}
        .kpi-card {{ flex: 1; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 5px solid #2b6cb0; text-align: center; }}
        .kpi-card .val {{ font-size: 28px; font-weight: bold; color: #2b6cb0; margin-top: 5px; }}
        .kpi-card .title {{ font-size: 13px; color: #64748b; text-transform: uppercase; font-weight: 600; }}
        .chart-box, .table-box {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }}
        th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background-color: #f1f5f9; color: #334155; font-weight: 600; }}
        tr:hover {{ background-color: #f8fafc; }}
        .footer {{ text-align: center; padding: 25px 20px; font-size: 13px; color: #475569; border-top: 1px solid #e2e8f0; margin-top: 30px; background: white; border-radius: 10px; }}
        .pix-box {{ font-weight: bold; color: #0284c7; margin-bottom: 6px; font-size: 14px; }}
    </style>
</head>
<body>

    <div class="header-card">
        {html_logo_tag}
        <h1>📊 Relatório DEMO - Atendimentos & Suporte</h1>
        <div class="account-badge">👤 Conta Simulado: {self.nome_conta_outlook}</div>
        
        <div class="params-box">
            <strong>⚙️ Parâmetros Utilizados na Consulta:</strong><br>
            • <strong>Período de Análise:</strong> {self.data_inicio} até {self.data_fim}<br>
            • <strong>Agrupamento Temporal:</strong> Por {granularidade}<br>
            • <strong>Gráfico das Ocorrências:</strong> Exibição em {tipo_grafico}<br>
            • <strong>Filtros Aplicados:</strong> Itens com a palavra 'pessoal' foram ignorados.
        </div>
    </div>

    <div class="chart-box" style="border-top: 4px solid #2b6cb0;">
        <h2>🎯 Principais Ocorrências (% de Atendimento)</h2>
        {fig_principais.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>

    <div class="kpi-row">
        <div class="kpi-card">
            <div class="title">Total de Eventos (Fictícios)</div>
            <div class="val">{total_eventos}</div>
        </div>
        <div class="kpi-card">
            <div class="title">Horas Alocadas</div>
            <div class="val">{total_horas}h</div>
        </div>
        <div class="kpi-card">
            <div class="title">Total de Suportes Prestados</div>
            <div class="val">{total_suportes}</div>
        </div>
    </div>

    <div class="chart-box">
        {fig_cat.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>

    <div class="chart-box">
        {fig_tempo.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>

    <div class="table-box">
        <h3>🙋‍♂️ Quantidade de Suportes Atendidos por Pessoa</h3>
        <table>
            <thead>
                <tr>
                    <th>Pessoa Atendida</th>
                    <th>Qtd de Suportes Realizados</th>
                    <th>Horas Totais</th>
                </tr>
            </thead>
            <tbody>
                {rows_suporte_pessoa if rows_suporte_pessoa else '<tr><td colspan="3">Nenhum suporte registrado.</td></tr>'}
            </tbody>
        </table>
    </div>

    <div class="table-box">
        <h3>📋 Resumo Agrupado de Outros Eventos / Reuniões (Top 50 Acumulados)</h3>
        <table>
            <thead>
                <tr>
                    <th>Assunto Parecido</th>
                    <th>Organizador</th>
                    <th>Ocorrências</th>
                    <th>Horas Totais</th>
                </tr>
            </thead>
            <tbody>
                {rows_outros_resumo if rows_outros_resumo else '<tr><td colspan="4">Nenhum outro evento registrado.</td></tr>'}
            </tbody>
        </table>
    </div>

    <div class="table-box">
        <h3>📁 Lista Final Detalhada de Suportes</h3>
        <table>
            <thead>
                <tr>
                    <th>Data / Hora</th>
                    <th>Pessoa / Solicitante</th>
                    <th>Assunto Completo</th>
                    <th>Duração</th>
                </tr>
            </thead>
            <tbody>
                {rows_lista_suporte if rows_lista_suporte else '<tr><td colspan="4">Nenhum suporte no período.</td></tr>'}
            </tbody>
        </table>
    </div>

    <div class="footer">
        <div class="pix-box">💛 {PIX_MSG}</div>
        {html_qrcode_tag}
        <br>
        {COPYRIGHT_TEXT}<br>
        Relatório DEMO gerado por {PROGRAM_NAME} ({PROGRAM_VERSION}) em {datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")}.
    </div>

</body>
</html>
"""
        filename = f"Relatorio_DEMO_{self.data_inicio.replace('/','-')}_a_{self.data_fim.replace('/','-')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_code)
        
        return filename

if __name__ == "__main__":
    root = tk.Tk()
    app = OutlookAnalyticsAppDemo(root)
    root.mainloop()