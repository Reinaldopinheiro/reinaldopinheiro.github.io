# Atualização em 26/01/2026 11:28 (Horário de Brasília)

import os
import sys
import shutil
import subprocess
import tkinter as tk
import threading
import time
import webbrowser
import datetime

# === CONFIGURAÇÕES ===
usuario_github = "Reinaldopinheiro"
repositorio = "reinaldopinheiro.github.io"
arquivo_html = "boletim4.html"
mensagem_commit = "Atualiza boletim.html"
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise Exception("Token do GitHub não encontrado. Defina GITHUB_TOKEN no ambiente.")

repo_url = f"https://github.com/{usuario_github}/{repositorio}.git"

# Detecta pasta base correta (mesmo em executável)
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

repo_path = os.path.join(base_dir, repositorio)
arquivo_origem = os.path.join(base_dir, arquivo_html)

# === Interface gráfica ===
root = tk.Tk()
root.title("ENVIANDO Boletim para o GitHub - BY Reinaldo Pinheiro")

largura_janela = 300
altura_janela = 300
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)
root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

log_text = tk.Text(root, wrap=tk.WORD, font=("Courier", 9))
log_text.pack(expand=True, fill=tk.BOTH)

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=5)

fechar_btn = tk.Button(frame_botoes, text="Fechar (60s)", command=root.destroy, font=("Arial", 10), bg="red", fg="white")
abrir_local_btn = tk.Button(frame_botoes, text="Abrir boletim local", font=("Arial", 10), bg="blue", fg="white")

def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    root.update()

def countdown():
    for i in range(60, 0, -1):
        fechar_btn.config(text=f"Fechar ({i}s)")
        time.sleep(1)
    root.destroy()

def abrir_local(caminho):
    webbrowser.open(f"file:///{os.path.abspath(caminho)}")

def gerar_nome_arquivo(base_dir):
    timestamp = datetime.datetime.now().strftime("%d%m%y%H%M%S")
    base_nome = f"boletim-{timestamp}.html"
    caminho = os.path.join(base_dir, base_nome)
    contador = 1
    while os.path.exists(caminho):
        base_nome = f"boletim-{timestamp}_{contador}.html"
        caminho = os.path.join(base_dir, base_nome)
        contador += 1
    return caminho

def executar_processo():
    try:
        log("🔍 Verificando repositório local...")
        if not os.path.exists(repo_path):
            log("📥 Clonando repositório...")
            subprocess.run(["git", "clone", repo_url], cwd=base_dir, check=True)

        if not os.path.exists(os.path.join(repo_path, ".git")):
            raise Exception("❌ A pasta clonada não é um repositório Git válido.")

        log("✅ Repositório Git detectado.")

        if not os.path.exists(arquivo_origem):
            raise Exception(f"❌ Arquivo boletim.html não encontrado em: {arquivo_origem}")

        destino_html = os.path.join(repo_path, arquivo_html)
        log("📤 Copiando boletim.html para o repositório...")
        shutil.copyfile(arquivo_origem, destino_html)

        # --- NOVO BLOCO: limpa qualquer rebase e força sobrescrever ---
        log("🧹 Limpando estado de rebase (se existir)...")
        subprocess.run(["git", "rebase", "--abort"], cwd=repo_path, check=False)

        log("📤 Enviando boletim.html original para o GitHub (forçando sobrescrever)...")
        subprocess.run(["git", "fetch", "origin", "main"], cwd=repo_path, check=True)
        subprocess.run(["git", "reset", "--hard", "origin/main"], cwd=repo_path, check=True)
        subprocess.run(["git", "add", arquivo_html], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", mensagem_commit], cwd=repo_path, check=True)
        subprocess.run(["git", "push", "origin", "main", "--force"], cwd=repo_path, check=True)
        log("✅ Commit realizado e enviado com sucesso (forçado).")

        novo_caminho = gerar_nome_arquivo(repo_path)
        log(f"📦 Criando cópia renomeada: {os.path.basename(novo_caminho)}")
        shutil.copyfile(destino_html, novo_caminho)

        log("🚀 Enviando versão renomeada para o GitHub (forçando sobrescrever)...")
        subprocess.run(["git", "add", os.path.basename(novo_caminho)], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", mensagem_commit], cwd=repo_path, check=True)
        subprocess.run(["git", "push", "origin", "main", "--force"], cwd=repo_path, check=True)
        log("✅ Versão renomeada enviada com sucesso (forçado)!")

        abrir_local_btn.config(command=lambda: abrir_local(novo_caminho))
        abrir_local_btn.pack(side=tk.LEFT, padx=5)
        fechar_btn.pack(side=tk.LEFT, padx=5)
        threading.Thread(target=countdown, daemon=True).start()

    except subprocess.CalledProcessError as e:
        log(f"❌ Erro durante o processo: {e}")
        abrir_local_btn.pack(side=tk.LEFT, padx=5)
        fechar_btn.pack(side=tk.LEFT, padx=5)
        threading.Thread(target=countdown, daemon=True).start()
    except Exception as e:
        log(f"❌ Erro inesperado: {e}")
        abrir_local_btn.pack(side=tk.LEFT, padx=5)
        fechar_btn.pack(side=tk.LEFT, padx=5)
        threading.Thread(target=countdown, daemon=True).start()

threading.Thread(target=executar_processo, daemon=True).start()
root.mainloop()
