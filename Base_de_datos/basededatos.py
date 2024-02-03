import pyodbc
import base64

SERVER = 'localhost'
BD = 'Placas_de_video'
USUARIO = 'sa'
CONTRA = '123'

class BaseDeDatos():
    def __init__(self):
        self.conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+SERVER+ '; DATABASE='+BD+'; UID='+USUARIO+';PWD='+CONTRA+';')
        print('Se conecto a la base de datos')
        self.cursor = self.conexion.cursor()

    def mirarTabla(self,tabla = 'placas'):
        try:
            self.cursor.execute(f'SELECT id,nombre,link,marca,precio,imagen,id_tienda from {tabla} ORDER BY precio ASC')
            return list(self.cursor.fetchall())
        except:
            Exception()
    
    def insertarPlaca(self, nombre:str, precio:int, link:str, marca:str, tienda, imagen:bytes):

        print("Insertando placa...")
        try:
            print(tienda)
            self.cursor.execute('INSERT INTO placas (nombre, link, marca, precio, imagen, id_tienda) VALUES (?, ?, ?, ?, CONVERT(varbinary(max), ?), ?)', (nombre, link, marca, precio, imagen, tienda))
            self.conexion.commit()
            print("Placa de video guardada!")
            print(tienda)
        except Exception as e:
            print("No se pudo guardar la placa en la base de datos.", e)

    def buscarPlaca(self, placa: str):
        try:
            query = "SELECT id, nombre, link, marca, precio, imagen, id_tienda FROM placas WHERE nombre LIKE ? ORDER BY precio ASC"
            self.cursor.execute(query, ("%" + placa.replace(" ", "%") + "%",))

            return self.cursor.fetchall()
        except Exception as e:
            print(e)
    
    def buscarPorMarca(self, marca: str):
        try:
            query = "SELECT id, nombre, link, marca, precio, imagen, id_tienda FROM placas WHERE marca LIKE ? ORDER BY precio ASC"
            self.cursor.execute(query, ("%" + marca.replace(" ", "%") + "%",))

            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def vaciarTablaPlaca(self):
        self.cursor.execute('DELETE from placas')
        self.conexion.commit()

    def devolverTienda(self,id:int):
        self.cursor.execute(f"Select nombre from tienda WHERE id = {id}")
        return self.cursor.fetchone()[0].title()

    def cerrarConexion(self):
        self.conexion.close()

    def idTienda(self, tienda: str):
        tienda = tienda.lower()
        try:
            self.cursor.execute('SELECT id from tienda WHERE nombre = ?', (tienda))
            result = self.cursor.fetchone()
            if result:
                return int(result[0])
            else:
                self.cursor.execute('INSERT INTO tienda (nombre) VALUES (?)', (tienda))
                self.cursor.commit()
                self.cursor.execute('SELECT MAX(id) from tienda')
                return int(self.cursor.fetchone()[0])
        except Exception as e:
            print(f"Error en idTienda: {e}")

    def eliminarPlacasDeUnaTienda(self, tienda: str):
        try:
            id = self.idTienda(tienda)
            self.cursor.execute("DELETE FROM placas WHERE id_tienda = ?", (id,))
            self.cursor.commit()
            return 1
        except Exception as e:
            print(e)
            return -1
