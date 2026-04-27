import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app.core.selenium_bridge import safe_click, wait_until
from app.core.media_resolver import is_video_card, get_card_title


SECTION_SELECTOR = 'button[data-orientation="vertical"][aria-controls]'
CARD_SELECTOR = 'div[data-state="open"][role="region"] div.cursor-pointer'
PLAYER_SOURCE_SELECTOR = 'div[data-media-provider] video source[type="application/x-mpegurl"]'


def get_sections(driver):
    return driver.find_elements(By.CSS_SELECTOR, SECTION_SELECTOR)


def open_section(driver, index, log):
    sections = get_sections(driver)

    if index >= len(sections):
        return False

    section = sections[index]
    title = section.text.split("\n")[0].strip() or f"Módulo {index + 1}"

    state = section.get_attribute("data-state")

    if state != "open":
        log(f"📂 Abrindo seção: {title}")
        safe_click(driver, section)
        time.sleep(1)
    else:
        log(f"📂 Seção já aberta: {title}")

    return True


def get_video_cards(driver):
    cards = driver.find_elements(By.CSS_SELECTOR, CARD_SELECTOR)
    return [card for card in cards if is_video_card(card)]


def wait_player_m3u8(driver, timeout=25):
    def source_loaded(d):
        sources = d.find_elements(By.CSS_SELECTOR, PLAYER_SOURCE_SELECTOR)

        for source in sources:
            src = source.get_attribute("src")
            if src and ".m3u8" in src:
                return src

        return False

    return wait_until(driver, source_loaded, timeout)


def click_video_card(driver, index, log):
    cards = get_video_cards(driver)

    if index >= len(cards):
        return None, None

    card = cards[index]
    titulo = get_card_title(card, f"video_{index + 1}")

    log(f"🎬 Abrindo aula: {titulo}")

    safe_click(driver, card)
    time.sleep(2)

    url = wait_player_m3u8(driver)

    return titulo, url