from models.Contribuyente import Contribuyente


def get_contribuyentes(df):

    contribuyentes = []

    if df is not None:
        for index, row in df.iterrows():
            # Crear un objeto Contribuyente para cada fila
            contribuyente = Contribuyente(
                cuit_contribuyente=str(row['CuitEmpresa']),
                cliente=row['NombreEmpresa'],
                filtro=row['Procesar?'],
                usuario=row['CuitIngreso'],
                password=row['Clave'],
                id_proceso=row['IdProceso']
            )

            contribuyentes.append(contribuyente)

    return contribuyentes
