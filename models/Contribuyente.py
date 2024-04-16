class Contribuyente:
    def __init__(self, id_contribuyente, id_corrida, cuit_contribuyente, cliente, grupo, usuario, password, filtro):
        self.id_contribuyente = id_contribuyente
        self.id_corrida = id_corrida
        self.cuit_contribuyente = cuit_contribuyente
        self.cliente = cliente
        self.grupo = grupo
        self.usuario = usuario
        self.password = password
        self.filtro = filtro
        self.ubicacion_guardado = rf'C:\Users\WNS\PycharmProjects\DescargaDeudaCtasTributarias\data\test'
        self.ubicacion_temporal = rf'C:\Users\WNS\PycharmProjects\DescargaDeudaCtasTributarias\data\temp\{self.cuit_contribuyente}'

    def __str__(self):
        return f"CUIT: {self.cuit_contribuyente}, Cliente: {self.cliente}"
