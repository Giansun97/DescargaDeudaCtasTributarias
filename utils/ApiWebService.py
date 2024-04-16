import requests


class ApiWebService(object):
    """
    classdocs
    """

    def __init__(self, url, user, password):
        """
        Constructor
        """
        self.url = url
        self.user = user
        self.passwd = password
        self.token = ""
        self.id = 0

    def conectar(self):
        # url = 'http://localhost:8000/api/v1/AfipApi/login'
        auth = {
            'email': self.user,
            'password': self.passwd
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self.url + "login", json=auth, headers=headers)
        dato = response.json()
        # print(str(dato['status']) + "   -   " + str(dato['message']))

        self.token = str(dato['message'])
        idtmp = self.token.split('|')
        self.id = idtmp[0]

    def getRepresentante(self, contribuyente):
        headers = {
            "Authorization": "Bearer " + self.token,
            "accept": "application/json"
        }
        response = requests.get(
            self.url + "uno?value=" + contribuyente.cuit_contribuyente,
            headers=headers
        )

        dato = response.json()
        # print(dato)
        contribuyente.usuario = None
        contribuyente.password = None
        if (dato['message'] is not None) and (dato['message'] != 'Unauthenticated.'):
            contribuyente.usuario = dato['message']['cuit']
            contribuyente.password = dato['message']['password']

        return contribuyente

    def close(self):
        testigo = False
        auth = {
            'email': self.user,
            'id': self.id
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self.url + "logout", json=auth, headers=headers)
        dato = response.json()
        if dato['status'] == '200':
            testigo = True

        return testigo
