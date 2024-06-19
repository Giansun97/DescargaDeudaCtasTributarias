import os
import shutil
from utils import constants
import time
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook


def mover_archivos_de_carpeta_temp_a_directorio_final(contribuyente):
    renombrar_excel(contribuyente)
    mover_archivos_a_ubicacion_guardado(contribuyente)
    crear_excel_desde_csv(contribuyente)


def crear_excel_desde_csv(contribuyente):
    ubicacion_guardado = os.path.abspath(constants.UBICACION_GUARDADO)

    nombre_archivo_csv = (
        f'{contribuyente.cuit_contribuyente} - {contribuyente.cliente} - '
        f'Estado de Deuda Cuentas Tributarias.csv'
    )

    ubicacion_archivos_csv = os.path.join(ubicacion_guardado)
    ruta_archivo_csv = os.path.join(ubicacion_archivos_csv, nombre_archivo_csv)

    df = pd.read_csv(ruta_archivo_csv, delimiter=',')

    # Agregar el CUIT y el nombre del contribuyente como nuevas columnas
    df['CUIT'] = contribuyente.cuit_contribuyente
    df['NombreContribuyente'] = contribuyente.cliente

    df['Fecha de Vencimiento'] = pd.to_datetime(df['Fecha de Vencimiento'], dayfirst=True, errors='coerce')

    # Crear la nueva columna 'Estado'
    df['Estado'] = df['Fecha de Vencimiento'].apply(
        lambda x: 'No Categorizada' if pd.isna(x) else ('Vencida' if x < datetime.now() else 'No Vencida'))

    columnas_a_convertir = ['Saldo', 'Int. resarcitorios', 'Int. punitorios']

    for columna in columnas_a_convertir:
        df[columna] = df[columna].str.replace(".", "").str.replace(",", ".").astype(float)

    nombre_archivo_excel = (
        f'{contribuyente.cuit_contribuyente} - '
        f'{contribuyente.cliente} - '
        f'Estado de Deuda Cuentas Tributarias.xlsx'
    )

    ruta_archivo_excel = os.path.join(ubicacion_archivos_csv, nombre_archivo_excel)
    df.to_excel(ruta_archivo_excel, index=False)


def verificar_carpeta_temp():
    """

        Verifica que en la carpeta de origen no haya archivos, y si hay los elimina

    """

    time.sleep(1)
    archivos_en_carpeta_temp = os.listdir(constants.UBICACION_TEMPORAL)

    if len(archivos_en_carpeta_temp) > 0:
        existen_archivos = True

        for archivo in archivos_en_carpeta_temp:
            time.sleep(1)
            ruta_archivo = os.path.join(constants.UBICACION_TEMPORAL, archivo)
            os.remove(ruta_archivo)

        print("Se han eliminado archivos de la carpeta temporal.")

        time.sleep(1)

    else:
        pass


def mover_archivos_a_ubicacion_guardado(contribuyente):
    ubicacion_guardado = os.path.abspath(constants.UBICACION_GUARDADO)

    try:
        # Verificar si la carpeta de destino existe.
        if os.path.exists(ubicacion_guardado):

            # Creamos la direccion final donde se va a guardar el archivo
            destino_periodo = os.path.join(ubicacion_guardado, contribuyente.id_proceso)

            # Si no existe la direccion la creamos
            if not os.path.exists(destino_periodo):
                os.makedirs(destino_periodo)

            # Obtenemos la lista de archivos en la carpeta de origen
            archivos = os.listdir(constants.UBICACION_TEMPORAL)
            print(archivos)

            time.sleep(1)
            # print(archivos)

            # Movemos cada archivo a la carpeta destino
            for archivo in archivos:
                origen_path = os.path.join(constants.UBICACION_TEMPORAL, archivo)
                destino_path = os.path.join(destino_periodo, archivo)
                shutil.move(origen_path, destino_path)

            time.sleep(1)

            print("Archivos movidos exitosamente.")

        else:
            print("La ruta de guardado no existe")

    except Exception as e:
        print(f"Error al mover archivos: {e}")


def renombrar_excel(contribuyente):
    time.sleep(2)
    archivos_en_carpeta = os.listdir(constants.UBICACION_TEMPORAL)

    if len(archivos_en_carpeta) == 1:
        # Solo hay un archivo, obtenemos su nombre
        archivo = archivos_en_carpeta[0]
        print(archivo)

        # Obtengo la ruta completa del archivo PDF
        ruta_archivo = os.path.join(constants.UBICACION_TEMPORAL, archivo)

        nuevo_nombre = (
            f'{contribuyente.cuit_contribuyente} - {contribuyente.cliente} - '
            f'Estado de Deuda Cuentas Tributarias.csv'
        )

        # Obteniendo la ruta del nuevo nombre
        ruta_nuevo_nombre = os.path.join(constants.UBICACION_TEMPORAL, nuevo_nombre)

        # Renombrar el archivo
        os.rename(ruta_archivo, ruta_nuevo_nombre)

        time.sleep(2)

    else:
        print("No se encontró o hay más de un archivo en la carpeta.")


def renombrar_excel_falta_presentacion(contribuyente):
    time.sleep(2)
    archivos_en_carpeta = os.listdir(constants.UBICACION_TEMPORAL)

    if len(archivos_en_carpeta) == 1:
        # Solo hay un archivo PDF, obtenemos su nombre
        archivo = archivos_en_carpeta[0]

        # Obtengo la ruta completa del archivo PDF
        ruta_archivo = os.path.join(constants.UBICACION_TEMPORAL, archivo)

        nuevo_nombre = (
            f'{contribuyente.cuit_contribuyente} - {contribuyente.cliente} - Faltas de '
            f'Presentacion.csv'
        )

        # Obteniendo la ruta del nuevo nombre
        ruta_nuevo_nombre = os.path.join(constants.UBICACION_TEMPORAL, nuevo_nombre)

        # Renombrar el archivo
        os.rename(ruta_archivo, ruta_nuevo_nombre)

        time.sleep(2)

    else:
        print("No se encontró o hay más de un archivo en la carpeta.")


def registrar_resultado_excel(archivo_control, contribuyente, mensaje):
    try:
        wb = load_workbook(archivo_control)
        ws = wb.active

        # Agregar una nueva fila con los valores obtenidos
        nueva_fila = [contribuyente.cuit_contribuyente, contribuyente.cliente, mensaje]

        ws.append(nueva_fila)
        wb.save(archivo_control)
        wb.close()

    except Exception as e:
        print(f"Error al registrar resultado en el archivo Excel: {e}")