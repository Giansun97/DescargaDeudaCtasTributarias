class Contribuyente:
    def __init__(self, cuit_contribuyente, cliente, usuario, password, filtro, id_proceso):

        self.cuit_contribuyente = cuit_contribuyente
        self.cliente = cliente
        self.usuario = usuario
        self.password = password
        self.filtro = filtro
        self.id_proceso = id_proceso

    def __str__(self):
        return f"CUIT: {self.cuit_contribuyente}, Cliente: {self.cliente}"
