import pandas as pd
from models.Contribuyente import Contribuyente
from utils import constants
from utils.ApiWebService import ApiWebService


def get_contribuyentes(df):

    contribuyentes = []

    if df is not None:
        for index, row in df.iterrows():
            # Crear un objeto Contribuyente para cada fila
            contribuyente = Contribuyente(
                id_contribuyente=int(row['id_contribuyente']),
                id_corrida=str(row['id_corrida']),
                cuit_contribuyente=str(row['cuit_contribuyente']),
                cliente=row['cliente'],
                grupo=row['grupo'],
                filtro=row['filtro'],
                usuario='',
                password=''
            )

            contribuyentes.append(contribuyente)

    return contribuyentes


def obtener_usuario_y_clave_bbdd(contribuyente: Contribuyente):
    api = ApiWebService(constants.BBDD_API_URL, constants.USER_API, constants.PASSWORD_API)
    api.conectar()
    contribuyente = api.getRepresentante(contribuyente)
    api.close()

    return contribuyente
