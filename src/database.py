import sqlite3
from utils import constants
import os
import pandas as pd


def cargar_resultado_en_database(contribuyente, resultado_proceso, cantidad_faltas_presentacion):
    # Almacena el resultado en la base de datos
    conn = sqlite3.connect(constants.DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO resultados_proceso (
            id_contribuyente,
            id_proceso,
            cantidad_faltas_presentacion,
            resultado_proceso
            
        ) VALUES (?, ?, ?, ?)
        """,
        (
            contribuyente.id_contribuyente,
            str(contribuyente.id_corrida),
            cantidad_faltas_presentacion,
            resultado_proceso
        )
    )

    conn.commit()
    conn.close()


def crear_tabla_resultado():
    # Crea la tabla de resultados si no existe
    conn = sqlite3.connect(constants.DB_PATH)
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS resultados_proceso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_contribuyente INTEGER,
            id_proceso TEXT,
            cantidad_faltas_presentacion INTEGER,
            resultado_proceso TEXT,
            time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_contribuyente) REFERENCES contribuyentes(id_contribuyente)
        )
        """
    )

    conn.commit()
    conn.close()


def crear_tabla_contribuyentes():
    # Crea la tabla de resultados si no existe
    conn = sqlite3.connect(constants.DB_PATH)
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS contribuyentes (
        id_contribuyente INTEGER,
        cuit_contribuyente TEXT,
        cliente TEXT,
        grupo TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def crear_tabla_deuda_contribuyentes():
    # Crea la tabla de resultados si no existe
    conn = sqlite3.connect(constants.DB_PATH)
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS deuda_contribuyentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Impuesto TEXT,
        Concepto_Subconcepto TEXT,
        Ant_Cuota TEXT,
        Período_Fiscal TEXT,
        Fecha_de_Vencimiento DATETIME,
        Saldo DECIMAL,
        Int_resarcitorios DECIMAL,
        Int_punitorios DECIMAL, 
        id_contribuyente INTEGER,
        id_proceso TEXT,
        
        FOREIGN KEY(id_contribuyente) REFERENCES contribuyentes(id_contribuyente)
        )
        """
    )

    conn.commit()
    conn.close()


def cargar_resultados_en_db(path):
    archivo = 'resultado.xlsx'

    complete_path = os.path.join(path, archivo)
    df = pd.read_excel(complete_path)
    df = df.rename(columns={
        'Concepto / Subconcepto': 'Concepto_Subconcepto',
        'Ant. / Cuota': 'Ant_Cuota',
        'Período Fiscal': 'Período_Fiscal',
        'Fecha de Vencimiento': 'Fecha_de_Vencimiento',
        'Int. resarcitorios': 'Int_Resarcitorios',
        'Int. punitorios': 'Int_Punitorios'
    })

    # Lista de nombres de columnas a eliminar
    columnas_a_eliminar = ["CUIT", "NombreContribuyente", "Grupo", "Estado"]

    # Eliminar las columnas del DataFrame
    df = df.drop(columns=columnas_a_eliminar)

    conn = sqlite3.connect(f'{constants.DB_PATH}')  # Reemplaza con la ruta correcta a tu base de datos
    df.to_sql('deuda_contribuyentes', conn, if_exists='append', index=False)
    conn.close()


# # configuracion
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.expand_frame_repr', False)
# pd.set_option('max_colwidth', 800)
#
# path = r'C:\Users\WNS\PycharmProjects\DescargaDeudaCtasTributarias\data\test\2024-04-15'
# cargar_resultados_en_db(path)
