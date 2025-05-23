import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def seleccionar_servicio(browser):
    _hacer_click_en_ver_todos(browser)
    _hacer_click_en_servicio(browser)
    time.sleep(2)


def _hacer_click_en_ver_todos(browser):
    VER_TODOS_XPATH = "//a[text()='Ver todos']"

    # Click ver todos button.
    ver_todos_button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, VER_TODOS_XPATH)))
    ver_todos_button.click()


def _hacer_click_en_servicio(browser):
    SERVICIO_XPATH = "//h3[contains(@class, 'roboto-font bold h5') and text()='SISTEMA DE CUENTAS TRIBUTARIAS']"

    # Seleccionar servicio Portal IVA
    servicio_button = WebDriverWait(browser, 20).until(EC.visibility_of_element_located(
        (By.XPATH, SERVICIO_XPATH)))

    # servicio_button.location_once_scrolled_into_view
    browser.execute_script("arguments[0].scrollIntoView();", servicio_button)
    time.sleep(2)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, SERVICIO_XPATH))).click()

    time.sleep(2)
