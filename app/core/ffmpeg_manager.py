import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
import tempfile


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.getcwd()


def encontrar_ffmpeg():
    local_ffmpeg = os.path.join(app_dir(), "ffmpeg.exe")

    if os.path.exists(local_ffmpeg):
        return local_ffmpeg

    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "ffmpeg"
    except Exception:
        return None


def instalar_ffmpeg(log=None):
    try:
        destino = os.path.join(app_dir(), "ffmpeg.exe")

        if os.path.exists(destino):
            if log:
                log("✅ FFmpeg já está instalado")
            return destino

        if log:
            log("⬇️ Baixando FFmpeg, aguarde alguns segundos...")

        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "ffmpeg.zip")

        urllib.request.urlretrieve(url, zip_path)

        if log:
            log("📦 Extraindo FFmpeg...")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        for root_dir, dirs, files in os.walk(temp_dir):
            if "ffmpeg.exe" in files:
                origem = os.path.join(root_dir, "ffmpeg.exe")
                shutil.copy(origem, destino)

                if log:
                    log("✅ FFmpeg instalado com sucesso!")

                return destino

        if log:
            log("❌ ffmpeg.exe não encontrado no ZIP")

        return None

    except Exception as e:
        if log:
            log(f"❌ Erro ao instalar FFmpeg: {e}")
        return None


def baixar_com_ffmpeg(url, output, log=None):
    ffmpeg = encontrar_ffmpeg()

    if not ffmpeg:
        if log:
            log("❌ FFmpeg não encontrado. Clique em FFmpeg Check para instalar.")
        return False

    cmd = [
        ffmpeg,
        "-y",
        "-i", url,
        "-c", "copy",
        output
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            if log:
                log("❌ Erro no FFmpeg")
                log(result.stderr[-500:])
            return False

        return True

    except Exception as e:
        if log:
            log(f"❌ Erro ao executar FFmpeg: {e}")
        return False