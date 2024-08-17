import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'balines'
)

sql = db.cursor()

def agregarReserva(idSucursal: int, idPromo: int, fechaInicio: list[int], fechaFin: list[int], nombreCliente: str, balasExtras: int) -> None:
    
    
    
    pass