import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from src.guardar_y_mover_archivos_descargados import mover_archivos_de_carpeta_temp_a_directorio_final
from src.guardar_y_mover_archivos_descargados import verificar_carpeta_temp, renombrar_excel_falta_presentacion
from src.guardar_y_mover_archivos_descargados import mover_archivos_a_ubicacion_guardado
from models.Contribuyente import Contribuyente


def descargar_deuda_contribuyente(driver, contribuyente: Contribuyente):
    """
        Gestiona el proceso principal que se realiza en la página de Sistema de Cuentas Tributarias

        :param driver: Selenium ChromeDriver
        :param contribuyente: Contribuyente

    """
    _cambiar_pestana(driver)

    # Cerrar el popup que aparece al abrir la pestaña de cuentas tributarias
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "close"))
    )

    close_button.click()

    select_element = verificar_existencia_seleccion_cliente(driver)

    if select_element:
        seleccionar_cuit_contribuyente(contribuyente, driver)

    # Descarga excel cuentas tributarias
    verificar_carpeta_temp()
    descargar_excel(driver)
    print("Se ha descargado el archivo de cuentas tributarias.")
    mover_archivos_de_carpeta_temp_a_directorio_final(contribuyente)
    print("Se ha movido el archivo de cuentas tributarias a la carpeta de destino.")

    # Descarga excel falta de presentaciones
    cantidad_faltas_de_presentacion = click_faltas_de_presentacion(driver)
    print(f"Cantidad de faltas de presentacion: {cantidad_faltas_de_presentacion}")
    verificar_carpeta_temp()
    faltas_de_presentacion_exist = descargar_excel_falta_presentacion(driver)
    print("Se ha descargado el archivo de faltas de presentacion.")

    if faltas_de_presentacion_exist:
        renombrar_excel_falta_presentacion(contribuyente)
        mover_archivos_a_ubicacion_guardado()

    return cantidad_faltas_de_presentacion


def verificar_existencia_seleccion_cliente(driver):
    try:
        # Esperar un momento para que se cargue la página
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "$PropertySelection")))

        select_element = True

    except Exception:
        select_element = False

    return select_element


def click_faltas_de_presentacion(driver):
    # Encontrar el botón de Excel usando XPath
    falta_de_presentacion_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.NAME, "functor$1")
    ))

    cantidad_faltas_presentacion = falta_de_presentacion_button.get_attribute("value")

    # # Hacer clic en el botón de Excel
    falta_de_presentacion_button.click()

    return cantidad_faltas_presentacion


def descargar_excel_falta_presentacion(driver):

    try:
        # Intentar encontrar el elemento
        elemento = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='value' and @name='label' and contains(text(), 'No se encontraron datos')]"))
        )

        print("El contribuyente no posee faltas de presentación.")

        faltas_de_presentacion_exist = False

    except TimeoutException:
        # Si el elemento no se encuentra, continuar con el programa
        print("El contribuyente posee Faltas de presentacion")
        faltas_de_presentacion_exist = True

    if faltas_de_presentacion_exist:
        # Encontrar el botón de Excel usando XPath
        excel_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, "//a[contains(@class, 'dt-button') and contains(., 'Excel')]")
        ))

        # Hacer clic en el botón de Excel
        excel_button.click()

    return faltas_de_presentacion_exist


def descargar_excel(driver):
    time.sleep(1)
    # Encontrar el botón de Excel usando XPath
    excel_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(), 'CSV')]")
    ))

    # Hacer clic en el botón de Excel
    excel_button.click()


def seleccionar_cuit_contribuyente(contribuyente, driver):

    # Esperar un momento para que se cargue la página
    select_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "$PropertySelection")))

    # Hacer clic en el elemento select para mostrar todas las opciones
    select_element.click()

    # Esperar a que todas las opciones estén disponibles
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "option")))

    # Encontrar el elemento select de nuevo ahora que todas las opciones están disponibles
    select = Select(select_element)

    # Obtener el CUIT del contribuyente
    selected_cuit = contribuyente.cuit_contribuyente

    # Seleccionar la opción que coincide con el CUIT del contribuyente
    select.select_by_visible_text(selected_cuit)

    print(f"Se ha seleccionado el CUIT {selected_cuit}.")


def _cambiar_pestana(driver):
    window_handles = driver.window_handles
    new_popup_handle = window_handles[-1]
    time.sleep(1)
    driver.switch_to.window(new_popup_handle)
    time.sleep(0.5)
