import os
import time
import threading
import subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib.request
import zipfile
import shutil
import tempfile

# =========================
# 🎨 UI MODERNA
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

driver = None
pasta_destino = os.getcwd()
ffmpeg_path = None


# =========================
# 🧾 LOG
# =========================
def log(msg):
    log_box.insert("end", msg + "\n")
    log_box.see("end")


# =========================
# 🔍 FFMPEG
# =========================
def encontrar_ffmpeg():
    if os.path.exists("ffmpeg.exe"):
        return "ffmpeg.exe"
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "ffmpeg"
    except:
        return None


def instalar_ffmpeg():
    try:
        log("⬇️ Baixando FFmpeg...")

        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "ffmpeg.zip")

        urllib.request.urlretrieve(url, zip_path)

        log("📦 Extraindo...")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        for root_dir, dirs, files in os.walk(temp_dir):
            if "ffmpeg.exe" in files:
                shutil.copy(os.path.join(root_dir, "ffmpeg.exe"), os.getcwd())
                log("✅ FFmpeg instalado!")
                return

        log("❌ FFmpeg não encontrado")

    except Exception as e:
        log(f"❌ Erro: {e}")


# =========================
# 🌐 NAVEGADOR
# =========================
def abrir_navegador():
    global driver

    try:
        if driver:
            log("⚠️ Já aberto")
            return

        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get(entry_url.get())
        log("🌐 Navegador aberto")

    except Exception as e:
        log(f"❌ Erro: {e}")


def login_feito():
    log("✅ Login confirmado")


# =========================
# 📁 PASTA
# =========================
def escolher_pasta():
    global pasta_destino
    pasta_destino = filedialog.askdirectory()
    log(f"📁 Pasta: {pasta_destino}")


# =========================
# ⬇️ DOWNLOAD
# =========================
def processo_download():
    global ffmpeg_path

    ffmpeg_path = encontrar_ffmpeg()

    if not ffmpeg_path:
        log("❌ FFmpeg não encontrado")
        return

    wait = WebDriverWait(driver, 20)

    log("🔍 Buscando vídeos...")

    containers = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cursor-pointer"))
    )

    total = len(containers)
    progress.set(0)

    for i in range(total):
        try:
            containers = driver.find_elements(By.CSS_SELECTOR, "div.cursor-pointer")
            container = containers[i]

            titulo = container.text.split("\n")[0].strip().replace("/", "-")

            log(f"🎬 {titulo}")

            driver.execute_script("arguments[0].scrollIntoView(true);", container)

            try:
                container.click()
            except:
                driver.execute_script("arguments[0].click();", container)

            video = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video source"))
            )

            url_video = video.get_attribute("src")

            if not url_video:
                log("❌ Sem link")
                continue

            arquivo_saida = os.path.join(pasta_destino, f"{titulo}.mp4")

            if os.path.exists(arquivo_saida):
                log("⏩ Já existe")
                continue

            log("⬇️ Baixando...")

            subprocess.run([
                ffmpeg_path,
                "-y",
                "-i", url_video,
                "-c", "copy",
                arquivo_saida
            ])

            progress.set((i + 1) / total)

            log("✅ Concluído")

        except Exception as e:
            log(f"⚠️ Erro: {e}")

    log("🏁 Finalizado!")


def iniciar_download():
    threading.Thread(target=processo_download, daemon=True).start()


# =========================
# 🖥️ UI MODERNA
# =========================
root = ctk.CTk()
root.title("Downloader PRO")
root.geometry("750x600")


# URL
entry_url = ctk.CTkEntry(root, width=500, placeholder_text="Cole a URL aqui...")
entry_url.pack(pady=15)


# BOTÕES
ctk.CTkButton(root, text="🌐 Abrir Navegador", command=abrir_navegador).pack(pady=5)
ctk.CTkButton(root, text="🔐 Login feito", command=login_feito).pack(pady=5)
ctk.CTkButton(root, text="📁 Escolher pasta", command=escolher_pasta).pack(pady=5)

ctk.CTkButton(
    root,
    text="⚙️ Instalar FFmpeg",
    command=lambda: threading.Thread(target=instalar_ffmpeg, daemon=True).start()
).pack(pady=5)

ctk.CTkButton(
    root,
    text="⬇️ BAIXAR CURSO",
    fg_color="green",
    hover_color="#0a8f3c",
    command=iniciar_download
).pack(pady=10)


# PROGRESS
progress = ctk.CTkProgressBar(root, width=600)
progress.set(0)
progress.pack(pady=10)


# LOGS
log_box = ctk.CTkTextbox(root, width=700, height=250)
log_box.pack(pady=10)


# START
root.mainloop()