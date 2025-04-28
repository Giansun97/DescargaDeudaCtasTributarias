from src.inicializar_navegador import inicializar_navegador
from src.ingresar_afip import ingresar_credenciales, cerrar_sesion_contribuyente
from src.seleccionar_servicio import seleccionar_servicio
from src.cuentas_tributarias.proceso_en_cuentas_tributarias import descargar_deuda_contribuyente
from utils.obtener_contribuyentes_a_procesar import get_contribuyentes
from src.guardar_y_mover_archivos_descargados import registrar_resultado_excel
from src.generar_reporte import generar_reporte
from src.database import crear_tabla_resultado
import pandas as pd
import time
from utils import constants
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox


def procesar_contribuyente(contribuyente):
    if contribuyente.filtro == 'Si':

        resultado_proceso = ''
        cantidad_faltas_presentacion = ''

        try:
            print(f"Procesando Contribuyente: {contribuyente}")
            # contribuyente = obtener_usuario_y_clave_bbdd(contribuyente)

            ubicacion_temporal = './data/temp'

            # Creamos la ubicacion temporal para la corrida.
            if not os.path.exists(ubicacion_temporal):
                os.makedirs(ubicacion_temporal)

            driver = inicializar_navegador()
            ingresar_credenciales(driver, contribuyente)
            seleccionar_servicio(driver)
            cantidad_faltas_presentacion = descargar_deuda_contribuyente(driver, contribuyente)
            print(f"Cantidad de faltas de presentacion: {cantidad_faltas_presentacion}")
            cerrar_sesion_contribuyente(driver)

            driver.close()
            resultado_proceso = 'Proceso finalizado con exito'
            print(resultado_proceso)

        except Exception:

            resultado_proceso = 'Error al procesar el contribuyente'
            print(resultado_proceso)

            return contribuyente

        finally:

            registrar_resultado_excel(constants.ARCHIVO_CONTROL, contribuyente, resultado_proceso)


def main():
    start_time_script = time.time()

    df = pd.read_excel(
        './data/input/listado_contribuyentes_a_procesar.xlsx',
        usecols='A:F',
        skiprows=1
    )

    print(df)
    contribuyentes = get_contribuyentes(df)

    for contribuyente in contribuyentes:
        procesar_contribuyente(contribuyente)

    end_time_script = time.time()
    script_elapsed_time = end_time_script - start_time_script

    print(f"TIEMPO DE EJECUCION DEL SCRIPT: {script_elapsed_time}")


def seleccionar_carpeta_y_generar_reporte():
    carpeta = filedialog.askdirectory()
    if carpeta:
        try:
            generar_reporte(carpeta)
            messagebox.showinfo("Éxito", f"Reporte generado en {carpeta}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar el reporte: {e}")


root = ctk.CTk()
root.title("Descarga Deuda Cuentas Tributarias")
root.geometry("400x400")

ctk.set_appearance_mode("dark")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

iniciar_proceso_button = ctk.CTkButton(
    input_frame,
    text="Iniciar Descarga desde Cuentas Tributarias",
    command=main
)

iniciar_proceso_button.grid(row=2, column=0, columnspan=2, sticky="news", padx=10, pady=10)

generar_reporte_button = ctk.CTkButton(
    input_frame,
    text="Seleccionar Carpeta y Generar Reporte",
    command=seleccionar_carpeta_y_generar_reporte
)
generar_reporte_button.grid(row=1, column=0, columnspan=2, sticky="news", padx=10, pady=10)

root.mainloop()
