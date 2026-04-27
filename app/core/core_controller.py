import threading

from app.core.selenium_bridge import get_driver
from app.core.course_navigator import (
    get_sections,
    open_section,
    get_video_cards,
    click_video_card
)
from app.core.download_engine import baixar_video_m3u8


def baixar_aula_atual(log, progress, pasta_destino):
    def run():
        try:
            driver = get_driver()

            if not driver:
                log("❌ Navegador não iniciado")
                return

            log("🔍 Procurando vídeo atual...")

            from app.core.course_navigator import wait_player_m3u8

            url = wait_player_m3u8(driver)

            if not url:
                log("❌ Nenhum .m3u8 encontrado no player atual")
                return

            baixar_video_m3u8(url, "aula_atual", pasta_destino, log)

        except Exception as e:
            log(f"❌ Erro aula atual: {e}")

    threading.Thread(target=run, daemon=True).start()


def baixar_curso_completo(log, progress, pasta_destino):
    def run():
        try:
            driver = get_driver()

            if not driver:
                log("❌ Navegador não iniciado")
                return

            sections = get_sections(driver)

            if not sections:
                log("❌ Nenhuma seção encontrada")
                return

            log(f"📚 Seções encontradas: {len(sections)}")

            total_baixados = 0

            progress["value"] = 0
            progress["maximum"] = 1

            for section_index in range(len(sections)):
                try:
                    abriu = open_section(driver, section_index, log)

                    if not abriu:
                        continue

                    cards = get_video_cards(driver)

                    if not cards:
                        log("⚠️ Nenhum vídeo nessa seção")
                        continue

                    log(f"🎯 Vídeos na seção: {len(cards)}")

                    progress["maximum"] = len(cards)
                    progress["value"] = 0

                    for card_index in range(len(cards)):
                        try:
                            titulo, url = click_video_card(driver, card_index, log)

                            if not url:
                                log("⚠️ Aula sem .m3u8, pulando")
                                continue

                            sucesso = baixar_video_m3u8(
                                url,
                                titulo,
                                pasta_destino,
                                log
                            )

                            if sucesso:
                                total_baixados += 1

                            progress["value"] = card_index + 1

                        except Exception as e:
                            log(f"⚠️ Erro no vídeo {card_index + 1}: {e}")

                except Exception as e:
                    log(f"⚠️ Erro na seção {section_index + 1}: {e}")

            log(f"🏁 Finalizado. Vídeos baixados: {total_baixados}")

        except Exception as e:
            log(f"❌ Erro geral: {e}")

    threading.Thread(target=run, daemon=True).start()