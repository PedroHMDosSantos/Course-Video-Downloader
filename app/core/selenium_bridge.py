from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

_driver = None


def abrir_navegador(url):
    global _driver

    if _driver:
        _driver.get(url)
        return _driver

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=service, options=options)
    _driver.get(url)

    return _driver


def get_driver():
    return _driver


def scroll_to(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )


def safe_click(driver, element):
    scroll_to(driver, element)
    driver.execute_script("arguments[0].click();", element)


def wait_until(driver, condition, timeout=20):
    return WebDriverWait(driver, timeout).until(condition)