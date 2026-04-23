import os
import sys
import time
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib.request
import zipfile
import shutil
import tempfile

driver = None
pasta_destino = os.getcwd()
ffmpeg_path = None


# =========================
# 🔍 LOG NA INTERFACE
# =========================
def log2(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)


# =========================
# 🔍 ENCONTRAR FFMPEG
# =========================
def encontrar_ffmpeg():
    if os.path.exists("ffmpeg.exe"):
        return os.path.abspath("ffmpeg.exe")

    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "ffmpeg"
    except:
        return None


# =========================
# 📥 INSTALAR FFMPEG
# =========================
def instalar_ffmpeg():
    try:
        log2("⬇️ Baixando FFmpeg...")

        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "ffmpeg.zip")

        urllib.request.urlretrieve(url, zip_path)

        log2("📦 Extraindo...")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        for root_dir, dirs, files in os.walk(temp_dir):
            if "ffmpeg.exe" in files:
                shutil.copy(os.path.join(root_dir, "ffmpeg.exe"), "ffmpeg.exe")
                log2("✅ FFmpeg instalado com sucesso!")
                return

        log2("❌ FFmpeg não encontrado no zip")

    except Exception as e:
        log2(f"❌ Erro: {e}")


# =========================
# 🌐 ABRIR NAVEGADOR
# =========================
def abrir_navegador():
    global driver

    try:
        # Corrige problema no .exe (chromedriver)
        service = Service()
        driver = webdriver.Chrome(service=service)

        driver.get(entry_url.get())
        log2("🌐 Navegador aberto")

    except Exception as e:
        log2(f"❌ Erro ao abrir navegador: {e}")


# =========================
# 🔐 LOGIN FEITO
# =========================
def login_feito():
    log2("✅ Login confirmado, pronto pra baixar")


# =========================
# 🎬 ESPERAR VIDEO CARREGAR
# =========================
def esperar_video(wait):
    return wait.until(
        lambda d: d.execute_script("""
            let v = document.querySelector('video source');
            return v && v.src ? v.src : null;
        """)
    )


# =========================
# ⬇️ BAIXAR VÍDEOS
# =========================
def processo_download():
    global ffmpeg_path

    ffmpeg_path = encontrar_ffmpeg()

    if not ffmpeg_path:
        log2("❌ FFmpeg não encontrado!")
        return

    wait = WebDriverWait(driver, 20)

    log2("🔍 Procurando vídeos...")

    containers = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cursor-pointer"))
    )

    total = len(containers)
    progresso["maximum"] = total

    for i in range(total):
        try:
            # 🔥 evita stale element
            containers = driver.find_elements(By.CSS_SELECTOR, "div.cursor-pointer")
            container = containers[i]

            titulo = container.text.split("\n")[0].strip().replace("/", "-")

            log2(f"🎬 {titulo}")

            driver.execute_script("arguments[0].scrollIntoView(true);", container)
            time.sleep(1)

            # 🔥 click mais confiável
            driver.execute_script("arguments[0].click();", container)

            # 🔥 espera vídeo carregar sem sleep
            url_video = esperar_video(wait)

            if not url_video:
                log2("❌ Não achou link")
                continue

            arquivo_saida = os.path.join(pasta_destino, f"{titulo}.mp4")

            if os.path.exists(arquivo_saida):
                log2("⏩ Já existe, pulando")
                continue

            log2("⬇️ Baixando...")

            subprocess.run([
                ffmpeg_path,
                "-y",
                "-i", url_video,
                "-c", "copy",
                arquivo_saida
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            log2("✅ Concluído")

            progresso["value"] = i + 1

        except Exception as e:
            log2(f"⚠️ Erro: {e}")
            continue

    log2("🏁 Finalizado!")


# =========================
# 🚀 INICIAR DOWNLOAD
# =========================
def iniciar_download():
    threading.Thread(target=processo_download).start()


# =========================
# 📁 ESCOLHER PASTA
# =========================
def escolher_pasta():
    global pasta_destino
    pasta_destino = filedialog.askdirectory()
    log2(f"📁 Pasta: {pasta_destino}")


# =========================
# 🖥️ INTERFACE
# =========================
root = tk.Tk()
root.title("Downloader de Curso")
root.geometry("600x500")

entry_url = tk.Entry(root, width=70)
entry_url.pack(pady=5)

#✏️ PLACEHOLDER URL

def on_focus_in(event):
    if entry_url.get() == "COLE A URL DO CURSO AQUI":
        entry_url.delete(0, tk.END)
        entry_url.config(fg="black")

def on_focus_out(event):
    if entry_url.get() == "":
        entry_url.insert(0, "COLE A URL DO CURSO AQUI")
        entry_url.config(fg="gray")


entry_url.insert(0, "COLE A URL DO CURSO AQUI")
entry_url.config(fg="gray")

entry_url.bind("<FocusIn>", on_focus_in)
entry_url.bind("<FocusOut>", on_focus_out)

tk.Button(root, text="🌐 Abrir Navegador", command=abrir_navegador).pack(pady=5)
tk.Button(root, text="🔐 Já fiz login", command=login_feito).pack(pady=5)
tk.Button(root, text="📁 Escolher pasta", command=escolher_pasta).pack(pady=5)
tk.Button(root, text="⚙️ Instalar FFmpeg", command=lambda: threading.Thread(target=instalar_ffmpeg).start()).pack(pady=5)
tk.Button(root, text="⬇️ Baixar Curso", command=iniciar_download).pack(pady=10)

progresso = ttk.Progressbar(root, length=500)
progresso.pack(pady=10)

log_text = tk.Text(root, height=15)
log_text.pack()

root.mainloop()