import re


def is_video_card(card):
    try:
        text = (card.text or "").lower()
        html = (card.get_attribute("innerHTML") or "").lower()

        if "publicação" in text:
            return False

        if "lucide-text" in html:
            return False

        if "lucide-play" in html:
            return True

        if re.search(r"\d+\s*min", text):
            return True

        if ".mp4" in html:
            return True

        return False

    except Exception:
        return False


def get_card_title(card, fallback="video"):
    try:
        title = card.find_element("css selector", "h5").text.strip()
        return title or fallback
    except Exception:
        return fallback