import os
import re

from app.core.ffmpeg_manager import baixar_com_ffmpeg


def limpar_nome(nome):
    nome = nome.strip()
    nome = re.sub(r'[\\/:*?"<>|]', "-", nome)
    nome = re.sub(r"\s+", " ", nome)
    return nome[:120] or "video"


def baixar_video_m3u8(url, titulo, pasta_destino, log):
    nome_limpo = limpar_nome(titulo)
    output = os.path.join(pasta_destino, f"{nome_limpo}.mp4")

    if os.path.exists(output):
        log(f"⏩ Já existe: {nome_limpo}.mp4")
        return True

    log(f"⬇️ Baixando: {nome_limpo}")

    sucesso = baixar_com_ffmpeg(url, output, log)

    if sucesso:
        log(f"✅ Concluído: {nome_limpo}.mp4")
    else:
        log(f"❌ Falhou: {nome_limpo}")

    return sucesso