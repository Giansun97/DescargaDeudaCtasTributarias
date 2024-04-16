from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils import constants


def configurar_opciones_chrome(contribuyente):
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option(
        "prefs", {
            "download.default_directory": contribuyente.ubicacion_temporal,
            "download.prompt_for_download": False,
            "profile.managed_default_content_settings.images": 2,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            'build': 'Python Sample Build',

        }
    )

    chrome_options.add_argument("--start-maximized")

    return chrome_options


def inicializar_navegador(contribuyente):
    chrome_options = configurar_opciones_chrome(contribuyente)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
