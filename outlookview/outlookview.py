# ================================================================================
# NOME DO PROGRAMA: Outlook Calendar & Support Analytics App
# VERSÃO: 1.0.7 (Filtro de datas robusto e compatível com MAPI/COM)
# DATA DE ATUALIZAÇÃO: 21 de Julho de 2026
# COPYRIGHT: Reinaldo Pinheiro 2026
# ================================================================================

import os
import sys
import re
import webbrowser
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    import pandas as pd
    import plotly.express as px
    import win32com.client
except ImportError as e:
    print(f"Erro ao importar bibliotecas: {e}")
    print("Execute: pip install pywin32 pandas plotly")

# --------------------------------------------------------------------------------
# CONSTANTES DE IDENTIFICAÇÃO DO SISTEMA
# --------------------------------------------------------------------------------
PROGRAM_NAME = "Outlook Calendar & Support Analytics App"
PROGRAM_VERSION = "v1.0.7"
PROGRAM_DATE = "21/07/2026"
COPYRIGHT_TEXT = "Copyright © Reinaldo Pinheiro 2026. Todos os direitos reservados."

class OutlookAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{PROGRAM_NAME} - {PROGRAM_VERSION}")
        self.root.geometry("640x540")
        self.root.resizable(False, False)
        
        self.data_inicio = "01/01/2026"
        self.data_fim = datetime.datetime.now().strftime("%d/%m/%Y")
        self.ultimo_html_gerado = None
        self.nome_conta_outlook = "Não Identificada"

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.bg_color = "#f4f6f9"
        self.primary_color = "#0056b3"
        
        self.root.configure(bg=self.bg_color)
        
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Header.TLabel", font=("Segoe UI", 15, "bold"), foreground=self.primary_color, background=self.bg_color)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9, "italic"), foreground="#64748b", background=self.bg_color)
        self.style.configure("Info.TLabel", font=("Segoe UI", 10), foreground="#334155", background=self.bg_color)
        self.style.configure("Copyright.TLabel", font=("Segoe UI", 8, "bold"), foreground="#64748b", background="#e2e8f0")
        
        self.style.configure("Main.TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def create_widgets(self):
        header_frame = ttk.Frame(self.root, padding="15 15 15 10")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text=PROGRAM_NAME, style="Header.TLabel").pack(anchor=tk.CENTER)
        
        info_version_text = f"Versão: {PROGRAM_VERSION}  |  Data de Atualização: {PROGRAM_DATE}"
        ttk.Label(header_frame, text=info_version_text, style="SubHeader.TLabel").pack(anchor=tk.CENTER, pady=(2, 10))

        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15)

        status_frame = ttk.Frame(self.root, padding="15 15 15 15")
        status_frame.pack(fill=tk.X)

        self.lbl_periodo = ttk.Label(
            status_frame, 
            text=f"📅 Período Selecionado: {self.data_inicio} até {self.data_fim}", 
            style="Info.TLabel",
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_periodo.pack(anchor=tk.CENTER, pady=5)

        self.lbl_status = ttk.Label(
            status_frame, 
            text="Pronto para realizar consultas na conta do Outlook Local.", 
            style="SubHeader.TLabel"
        )
        self.lbl_status.pack(anchor=tk.CENTER)

        btn_container = ttk.Frame(self.root, padding="20 10 20 10")
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
            text="🔄 Fazer Nova Consulta e Gerar Dashboard HTML", 
            style="Main.TButton",
            command=self.acao_gerar_consulta
        )
        self.btn_nova_consulta.pack(fill=tk.X, pady=4)

        self.btn_ver_html = ttk.Button(
            btn_container, 
            text="🌐 Ver o HTML Gerado no Navegador", 
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

        footer_frame = tk.Frame(self.root, bg="#e2e8f0", height=35)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        lbl_copy = ttk.Label(footer_frame, text=COPYRIGHT_TEXT, style="Copyright.TLabel")
        lbl_copy.pack(expand=True, pady=8)

    # ----------------------------------------------------------------------------
    # LEITURA DOS ARQUIVOS DE CONFIGURAÇÃO (.RPC)
    # ----------------------------------------------------------------------------
    def carregar_lista_rpc(self, nome_arquivo):
        lista = []
        if os.path.exists(nome_arquivo):
            try:
                with open(nome_arquivo, "r", encoding="utf-8") as f:
                    for line in f:
                        item = line.strip()
                        if item and not item.startswith("#"):
                            lista.append(item)
            except Exception as e:
                print(f"Aviso ao ler {nome_arquivo}: {e}")
        return lista

    # ----------------------------------------------------------------------------
    # EVENTOS DE BOTÃO
    # ----------------------------------------------------------------------------
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
        self.lbl_status.config(text="Lendo o calendário do Outlook...")
        self.root.update()

        try:
            df_eventos, nome_conta = self.extrair_dados_outlook()
            if df_eventos is None or df_eventos.empty:
                messagebox.showwarning("Sem Resultados", "Nenhum compromisso foi encontrado no período selecionado.")
                self.lbl_status.config(text="Consulta concluída: Sem dados.")
                return

            self.nome_conta_outlook = nome_conta
            html_file = self.gerar_dashboard_html(df_eventos)
            self.ultimo_html_gerado = html_file

            self.lbl_status.config(text=f"✅ Relatório gerado com sucesso!")
            
            resp = messagebox.askyesno("Consulta Concluída", f"Dashboard gerado com sucesso!\nConta: {nome_conta}\n\nDeseja abrir o relatório HTML agora?")
            if resp:
                self.acao_ver_html()

        except Exception as e:
            messagebox.showerror("Erro de Integração", f"Erro ao acessar o Outlook:\n{str(e)}")
            self.lbl_status.config(text="Erro de execução.")

    # ----------------------------------------------------------------------------
    # CONEXÃO COM O OUTLOOK E PROCESSAMENTO (CORRIGIDO)
    # ----------------------------------------------------------------------------
    def extrair_dados_outlook(self):
        palavras_ignorar = [p.lower() for p in self.carregar_lista_rpc("ignorar.rpc")]
        palavras_agrupar = self.carregar_lista_rpc("agrupar.rpc")

        try:
            outlook = win32com.client.Dispatch("Outlook.Application")
            namespace = outlook.GetNamespace("MAPI")
            
            nome_conta = "Conta Local Outlook"
            try:
                if namespace.Accounts.Count > 0:
                    nome_conta = namespace.Accounts.Item(1).SmtpAddress or namespace.Accounts.Item(1).DisplayName
                else:
                    nome_conta = namespace.CurrentUser.Name
            except Exception:
                nome_conta = "Conta do Usuário Local"

            calendar = namespace.GetDefaultFolder(9) # olFolderCalendar
            items = calendar.Items
            items.IncludeRecurrences = True
            items.Sort("[Start]")

            # Converte as datas de entrada em objetos datetime nativos
            dt_inicio_obj = datetime.datetime.strptime(f"{self.data_inicio} 00:00:00", "%d/%m/%Y %H:%M:%S")
            dt_fim_solicitado = datetime.datetime.strptime(f"{self.data_fim} 23:59:59", "%d/%m/%Y %H:%M:%S")
            
            # O limite máximo do estudo é o MOMENTO ATUAL
            agora = datetime.datetime.now()
            dt_limite_final = min(dt_fim_solicitado, agora)

            # Formatação de string de data legível e aceita globalmente pelo MAPI do Outlook
            str_inicio = dt_inicio_obj.strftime("%d/%m/%Y %H:%M")
            str_fim = dt_limite_final.strftime("%d/%m/%Y %H:%M")

            restriction = f"[Start] >= '{str_inicio}' AND [Start] <= '{str_fim}'"
            
            try:
                filtered_items = items.Restrict(restriction)
            except Exception:
                # Caso o Restrict falhe por idioma do SO, usa a coleção bruta
                filtered_items = items

            records = []
            for item in filtered_items:
                try:
                    # Garantia de acesso ao objeto do compromisso
                    if not hasattr(item, 'Start'):
                        continue

                    start_dt = item.Start
                    
                    # Converte a data do item para datetime sem fuso se necessário
                    if hasattr(start_dt, 'tzinfo') and start_dt.tzinfo is not None:
                        start_dt_naive = start_dt.replace(tzinfo=None)
                    else:
                        start_dt_naive = datetime.datetime(
                            start_dt.year, start_dt.month, start_dt.day,
                            start_dt.hour, start_dt.minute, start_dt.second
                        )

                    # Filtro manual extra para precisão absoluta (Ignora futuros e fora do intervalo)
                    if start_dt_naive < dt_inicio_obj or start_dt_naive > dt_limite_final:
                        continue

                    subject = item.Subject if hasattr(item, 'Subject') and item.Subject else "Sem Assunto"
                    organizer = item.Organizer if hasattr(item, 'Organizer') and item.Organizer else "Desconhecido"
                    
                    text_lower = subject.lower()

                    # 1. Ignorar se estiver no ignorar.rpc
                    if any(p in text_lower for p in palavras_ignorar):
                        continue

                    # 2. Verificar correspondência no agrupar.rpc
                    grupo_encontrado = "Outros"
                    for termo in palavras_agrupar:
                        if termo.lower() in text_lower:
                            grupo_encontrado = termo.title()
                            break

                    # 3. Classificação de Suportes / Reuniões
                    pessoa_atendida = organizer
                    if "suporte" in text_lower or any(w in text_lower for w in ["chamado", "ticket", "incidente"]):
                        categoria = "Suporte Técnico"
                        match = re.search(r'suporte\s+([a-zA-Zá-úÁ-Ú]+)', text_lower)
                        if match:
                            pessoa_atendida = match.group(1).capitalize()
                    elif any(w in text_lower for w in ["reunião", "meeting", "sync", "alinhamento"]):
                        categoria = "Reuniões Internas"
                    else:
                        categoria = "Outros Atendimentos"

                    duration_h = round(item.Duration / 60.0, 2) if hasattr(item, 'Duration') else 0.0

                    records.append({
                        "Assunto": subject,
                        "Inicio": start_dt_naive.strftime("%Y-%m-%d %H:%M"),
                        "Mes_Ano": start_dt_naive.strftime("%Y-%m"),
                        "Duracao_Horas": duration_h,
                        "Organizador": organizer,
                        "Pessoa_Atendida": pessoa_atendida,
                        "Categoria": categoria,
                        "Grupo_Agrupar": grupo_encontrado
                    })
                except Exception:
                    continue

            print(f"Total de registros recuperados do Outlook: {len(records)}")
            return pd.DataFrame(records), nome_conta

        except Exception as err:
            raise err

    # ----------------------------------------------------------------------------
    # CONSTRUÇÃO DO PAINEL HTML
    # ----------------------------------------------------------------------------
    def gerar_dashboard_html(self, df):
        df_agrupar = df[df['Grupo_Agrupar'] != "Outros"]
        if df_agrupar.empty:
            df_agrupar = df

        df_agrupar_summary = df_agrupar.groupby('Grupo_Agrupar').agg(
            Qtd_Ocorrencias=('Assunto', 'count'),
            Total_Horas=('Duracao_Horas', 'sum')
        ).reset_index()

        df_agrupar_summary['Rotulo_Legenda'] = df_agrupar_summary.apply(
            lambda r: f"{r['Grupo_Agrupar']} ({r['Qtd_Ocorrencias']}x)", axis=1
        )

        fig_principais = px.pie(
            df_agrupar_summary, 
            names='Rotulo_Legenda', 
            values='Total_Horas',
            title='<b>Principais Ocorrências (agrupar.rpc)</b>', 
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig_principais.update_traces(
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Horas Totais: %{value:.1f}h<br>Porcentagem: %{percent}"
        )
        fig_principais.update_layout(
            font=dict(family="Segoe UI, sans-serif"),
            legend_title_text="Ocorrência (Qtd)"
        )

        fig_cat = px.pie(
            df, names='Categoria', values='Duracao_Horas',
            title='<b>Distribuição de Horas por Categoria</b>', hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_cat.update_layout(font=dict(family="Segoe UI, sans-serif"))

        df_mes = df.groupby(['Mes_Ano', 'Categoria'])['Duracao_Horas'].sum().reset_index()
        fig_mes = px.bar(
            df_mes, x='Mes_Ano', y='Duracao_Horas', color='Categoria',
            title='<b>Evolução Mensal de Horas</b>', barmode='stack',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_mes.update_layout(font=dict(family="Segoe UI, sans-serif"))

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

        html_code = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Principais Ocorrências - {PROGRAM_NAME}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 20px; }}
        .header-card {{ background: linear-gradient(135deg, #0056b3, #1e3a8a); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        .header-card h1 {{ margin: 0 0 10px 0; font-size: 24px; }}
        .header-meta {{ font-size: 14px; opacity: 0.95; line-height: 1.6; }}
        .account-badge {{ display: inline-block; background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-weight: bold; margin-top: 10px; }}
        .kpi-row {{ display: flex; gap: 15px; margin-bottom: 25px; }}
        .kpi-card {{ flex: 1; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 5px solid #0056b3; text-align: center; }}
        .kpi-card .val {{ font-size: 28px; font-weight: bold; color: #0056b3; margin-top: 5px; }}
        .kpi-card .title {{ font-size: 13px; color: #64748b; text-transform: uppercase; font-weight: 600; }}
        .chart-box, .table-box {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }}
        th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background-color: #f1f5f9; color: #334155; font-weight: 600; }}
        tr:hover {{ background-color: #f8fafc; }}
        .footer {{ text-align: center; padding: 20px; font-size: 13px; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 30px; }}
    </style>
</head>
<body>

    <div class="header-card">
        <h1>📊 {PROGRAM_NAME}</h1>
        <div class="header-meta">
            <div><strong>Versão:</strong> {PROGRAM_VERSION} | <strong>Data da Versão:</strong> {PROGRAM_DATE}</div>
            <div><strong>Período Analisado:</strong> {self.data_inicio} até {self.data_fim} (Estritamente até a Data Atual)</div>
            <div class="account-badge">👤 Conta Outlook Conectada: {self.nome_conta_outlook}</div>
        </div>
    </div>

    <!-- GRÁFICO DE PIZZA LOGO NO INÍCIO: PRINCIPAIS OCORRÊNCIAS -->
    <div class="chart-box" style="border-top: 4px solid #2563eb;">
        <h2>🎯 Principais Ocorrências</h2>
        {fig_principais.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>

    <div class="kpi-row">
        <div class="kpi-card">
            <div class="title">Total de Eventos</div>
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
        {fig_mes.to_html(full_html=False, include_plotlyjs='cdn')}
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
        {COPYRIGHT_TEXT}<br>
        Relatório gerado por {PROGRAM_NAME} ({PROGRAM_VERSION}) em {datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")}.
    </div>

</body>
</html>
"""
        filename = f"Relatorio_Outlook_{self.data_inicio.replace('/','-')}_a_{self.data_fim.replace('/','-')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_code)
        
        return filename

if __name__ == "__main__":
    root = tk.Tk()
    app = OutlookAnalyticsApp(root)
    root.mainloop()