from src.inicializar_navegador import inicializar_navegador
from src.ingresar_afip import ingresar_credenciales, cerrar_sesion_contribuyente
from src.seleccionar_servicio import seleccionar_servicio
from src.cuentas_tributarias.proceso_en_cuentas_tributarias import descargar_deuda_contribuyente
from utils.obtener_contribuyentes_a_procesar import get_contribuyentes, obtener_usuario_y_clave_bbdd
from src.database import cargar_resultado_en_database, crear_tabla_resultado
import pandas as pd
import time
import concurrent.futures
import os


def procesar_contribuyente(contribuyente):
    if contribuyente.filtro == 'x':

        resultado_proceso = ''
        cantidad_faltas_presentacion = ''

        try:
            print(f"Procesando Contribuyente: {contribuyente}")
            contribuyente = obtener_usuario_y_clave_bbdd(contribuyente)

            # Creamos la ubicacion temporal para la corrida.
            if not os.path.exists(contribuyente.ubicacion_temporal):
                os.makedirs(contribuyente.ubicacion_temporal)

            driver = inicializar_navegador(contribuyente)
            ingresar_credenciales(driver, contribuyente)
            seleccionar_servicio(driver)
            cantidad_faltas_presentacion = descargar_deuda_contribuyente(driver, contribuyente)
            cerrar_sesion_contribuyente(driver)

            driver.close()
            resultado_proceso = 'Proceso finalizado con exito'

        except Exception:

            resultado_proceso = 'Error al procesar el contribuyente'
            return contribuyente

        finally:

            cargar_resultado_en_database(contribuyente, resultado_proceso, cantidad_faltas_presentacion)

        return None


def main():
    start_time_script = time.time()

    df = pd.read_excel('./data/input/input_contribuyentes.xlsx')
    contribuyentes = get_contribuyentes(df)

    # Creamos la tabla en la base de datos si no existe.
    crear_tabla_resultado()

    # for contribuyente in contribuyentes:
    #     procesar_contribuyente(contribuyente)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        resultados = executor.map(procesar_contribuyente, contribuyentes)
        contribuyentes_con_errores = [resultado for resultado in resultados if resultado is not None]

    # Reprocesar los contribuyentes que tuvieron errores
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(procesar_contribuyente, contribuyentes_con_errores)

    end_time_script = time.time()
    script_elapsed_time = end_time_script - start_time_script

    print(f"TIEMPO DE EJECUCION DEL SCRIPT: {script_elapsed_time}")


if __name__ == '__main__':
    main()
