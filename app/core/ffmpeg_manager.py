import os
import subprocess


def encontrar_ffmpeg():
    if os.path.exists("ffmpeg.exe"):
        return "ffmpeg.exe"

    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "ffmpeg"
    except Exception:
        return None


def baixar_com_ffmpeg(url, output, log=None):
    ffmpeg = encontrar_ffmpeg()

    if not ffmpeg:
        if log:
            log("❌ FFmpeg não encontrado")
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