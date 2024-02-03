from fastapi import FastAPI
from pydantic import BaseModel
from Base_de_datos.basededatos import BaseDeDatos
from fastapi.responses import JSONResponse
from base64 import b64encode
import operator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Configura CORS para permitir solicitudes desde la dirección de tu página web
origins = [
    "http://localhost:5500/pagina/index.html",
    "http://localhost",
    "http://localhost:5500"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  
    allow_headers=["*"],
)






@app.get('/')
def inicio():
    return {"bienvenido": "api web scraping - placas de video"}

@app.get('/placas/')
def get_placas(nombre:str='', marca:str=''):
    bd = BaseDeDatos()
    lista_de_placas = []
    if nombre == '' and marca == '':
        for placa in bd.mirarTabla():
            placa_dict = {
                "Nombre": placa[1],
                "Link": placa[2],
                "Marca": placa[3],
                "Precio": float(placa[4]),
                "Imagen": b64encode(placa[5]).decode('utf-8'),
                "Tienda": bd.devolverTienda(placa[6])
            }
            lista_de_placas.append(placa_dict)
    elif nombre != '' and marca == '':
        for placa in bd.buscarPlaca(nombre):
            placa_dict = {
                "Nombre": placa[1],
                "Link": placa[2],
                "Marca": placa[3],
                "Precio": float(placa[4]),
                "Imagen": b64encode(placa[5]).decode('utf-8'),
                "Tienda": bd.devolverTienda(placa[6])
            }
            lista_de_placas.append(placa_dict)

    bd.cerrarConexion()
    #lista_de_placas.sort(key=operator.itemgetter('Precio'))
    return JSONResponse(content=lista_de_placas)

@app.post('/post_placa/')
def post_placa(nombre,precio,link,marca,tienda,imagen):
    bd = BaseDeDatos()
    bd.insertarPlaca(nombre=nombre,precio=precio,link=link,marca=marca,tienda=bd.idTienda(tienda),imagen=imagen)
    bd.cerrarConexion()