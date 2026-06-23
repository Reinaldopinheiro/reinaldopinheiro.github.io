# =================================================================
# NOME: enviaboletim.py
# VERSÃO: 2.0 (Upload Web via FTP)
# AUTOR: Reinaldo Pinheiro & IA Gemini
# DESCRIÇÃO: Envia o arquivo HTML diretamente para o servidor do site.
# =================================================================

import ftplib
import os
from datetime import datetime

# --- CONFIGURAÇÕES DO SEU SERVIDOR (PREENCHA AQUI) ---
FTP_HOST = "ftp.seusite.com.br"    # Endereço do FTP
FTP_USER = "seu_usuario"           # Usuário do FTP
FTP_PASS = "sua_senha"             # Senha do FTP
FTP_DIR  = "public_html/boletim"   # Pasta dentro do servidor (ex: public_html)

ARQUIVO_LOCAL = "boletim4.html"    # Nome do arquivo no seu PC

def enviar_agora():
    """Conecta ao servidor e faz o upload do arquivo"""
    agora = datetime.now().strftime("%H:%M:%S")
    
    if not os.path.exists(ARQUIVO_LOCAL):
        print(f"[{agora}] ❌ Erro: Arquivo {ARQUIVO_LOCAL} não encontrado localmente.")
        return False

    try:
        print(f"[{agora}] 🌐 Conectando ao servidor {FTP_HOST}...")
        
        # Inicia a conexão FTP
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        # Tenta entrar na pasta destino (se não existir, você deve criar antes no servidor)
        try:
            ftp.cwd(FTP_DIR)
        except:
            print(f"[{agora}] ⚠️ Pasta {FTP_DIR} não encontrada no servidor.")
            # Opcional: ftp.mkd(FTP_DIR) # Tenta criar a pasta se tiver permissão
        
        # Abre o arquivo e faz o upload
        with open(ARQUIVO_LOCAL, "rb") as arquivo:
            print(f"[{agora}] 📤 Fazendo upload de {ARQUIVO_LOCAL}...")
            ftp.storbinary(f"STOR {ARQUIVO_LOCAL}", arquivo)
        
        ftp.quit()
        print(f"[{agora}] ✅ Sucesso! O boletim já está online no seu site.")
        return True

    except Exception as e:
        print(f"[{agora}] ❌ Falha no upload: {e}")
        return False

# Para teste manual
if __name__ == "__main__":
    enviar_agora()