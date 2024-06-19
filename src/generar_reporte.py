import pandas as pd
import os
from datetime import datetime

# configuracion
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)


def generar_reporte(path):

    archivos = os.listdir(path)

    dfs = []

    for archivo in archivos:

        if archivo.endswith('.xlsx') and 'Cuentas Tributarias' in archivo:
            complete_path = os.path.join(path, archivo)

            # Crear un DataFrame a partir de los datos de la hoja
            df = pd.read_excel(complete_path)

            # Reorganizamos las columnas del dataframe para que queden CUIT, NombreContribuyente y Grupo adelante
            nuevo_orden = (
                    ['CUIT', 'NombreContribuyente', 'Grupo'] +
                    [c for c in df.columns if c not in ['CUIT', 'NombreContribuyente', 'Grupo']]
            )

            # Reorganiza las columnas
            df = df.reindex(columns=nuevo_orden)

            # Añadir el DataFrame a la lista
            dfs.append(df)

    # Concatenar todos los DataFrames en uno solo
    resultado = pd.concat(dfs, ignore_index=True)
    resultado.to_excel(rf'{path}\resultado.xlsx', index=False, sheet_name='ReporteDeuda')

