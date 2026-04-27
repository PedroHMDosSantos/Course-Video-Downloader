import tkinter as tk
from tkinter import filedialog, ttk

from app.core.selenium_bridge import abrir_navegador
from app.core.core_controller import baixar_aula_atual, baixar_curso_completo
from app.core.ffmpeg_manager import encontrar_ffmpeg

pasta_destino = None


def create_app():
    root = tk.Tk()
    root.title("Downloader PRO")
    root.geometry("760x600")
    root.configure(bg="#121212")

    # =========================
    # GRID CONFIG PRINCIPAL
    # =========================
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # =========================
    # URL INPUT
    # =========================
    entry_url = tk.Entry(
        root,
        bg="#1e1e1e",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    entry_url.grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=15,
        pady=10,
        ipady=6
    )

    # =========================
    # LOG FUNCTION
    # =========================
    def log(msg):
        log_box.insert("end", msg + "\n")
        log_box.see("end")

    # =========================
    # FUNÇÕES
    # =========================
    def escolher_pasta():
        global pasta_destino
        pasta_destino = filedialog.askdirectory()

        if pasta_destino:
            log(f"📁 Pasta selecionada: {pasta_destino}")
        else:
            log("⚠️ Nenhuma pasta selecionada")

    def abrir():
        url = entry_url.get().strip()

        if not url:
            log("❌ Cole uma URL primeiro")
            return

        try:
            abrir_navegador(url)
            log("🌐 Navegador aberto")
        except Exception as e:
            log(f"❌ Erro ao abrir navegador: {e}")

    def login_feito():
        log("🔐 Login confirmado")
        log("✅ Agora vá até a página do curso/aula e escolha uma opção de download")

    def check_ffmpeg():
        ffmpeg = encontrar_ffmpeg()

        if ffmpeg:
            log(f"✅ FFmpeg OK: {ffmpeg}")
        else:
            log("❌ FFmpeg não encontrado")

    def baixar_atual():
        if not pasta_destino:
            log("❌ Escolha uma pasta primeiro")
            return

        log("⬇️ Iniciando download da aula atual...")
        baixar_aula_atual(log, progress, pasta_destino)

    def baixar_completo():
        if not pasta_destino:
            log("❌ Escolha uma pasta primeiro")
            return

        log("🚀 Iniciando modo curso completo...")
        baixar_curso_completo(log, progress, pasta_destino)

    # =========================
    # BOTÃO PADRÃO
    # =========================
    def btn(text, cmd, color="#2a2a2a", fg="white"):
        return tk.Button(
            root,
            text=text,
            command=cmd,
            bg=color,
            fg=fg,
            relief="flat",
            activebackground="#00c853",
            activeforeground="black"
        )

    # =========================
    # BOTÕES GRID
    # =========================
    btn("🌐 Abrir navegador", abrir).grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=15,
        pady=5,
        ipady=10
    )

    btn("🔐 Login feito", login_feito).grid(
        row=1,
        column=1,
        sticky="nsew",
        padx=15,
        pady=5,
        ipady=10
    )

    btn("📁 Escolher pasta", escolher_pasta).grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=15,
        pady=5,
        ipady=10
    )

    btn("⚙️ FFmpeg Check", check_ffmpeg).grid(
        row=2,
        column=1,
        sticky="nsew",
        padx=15,
        pady=5,
        ipady=10
    )

    # =========================
    # BAIXAR AULA ATUAL
    # =========================
    btn("⬇️ BAIXAR AULA ATUAL", baixar_atual, "#2a2a2a", "white").grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=15,
        pady=6,
        ipady=12
    )

    # =========================
    # BAIXAR CURSO COMPLETO
    # =========================
    btn("🚀 BAIXAR CURSO COMPLETO", baixar_completo, "#00c853", "black").grid(
        row=4,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=15,
        pady=8,
        ipady=12
    )

    # =========================
    # PROGRESS BAR
    # =========================
    global progress
    progress = ttk.Progressbar(root)
    progress.grid(
        row=5,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=15,
        pady=5
    )

    # =========================
    # DASHBOARD
    # =========================
    tk.Label(
        root,
        text="📊 Dashboard",
        bg="#121212",
        fg="white",
        font=("Segoe UI", 10, "bold")
    ).grid(
        row=6,
        column=0,
        columnspan=2,
        sticky="w",
        padx=15,
        pady=(10, 0)
    )

    # =========================
    # LOG BOX
    # =========================
    global log_box
    log_box = tk.Text(
        root,
        height=12,
        bg="#0d0d0d",
        fg="#00ff88",
        relief="flat"
    )
    log_box.grid(
        row=7,
        column=0,
        columnspan=2,
        sticky="nsew",
        padx=15,
        pady=5
    )

    # =========================
    # EXPANSÃO GRID
    # =========================
    root.rowconfigure(7, weight=1)

    return root