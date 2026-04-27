import json


def capturar_rede(driver):
    logs = driver.get_log("performance")
    urls = set()

    for entry in logs:
        try:
            msg = json.loads(entry["message"])["message"]

            if msg["method"] != "Network.responseReceived":
                continue

            url = msg["params"]["response"]["url"]

            if any(ext in url for ext in [".m3u8", ".mp4", ".mpd", ".ts"]):
                urls.add(url)

        except:
            pass

    return list(urls)