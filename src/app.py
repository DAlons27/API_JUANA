from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import config

from routes.auth import routes_auth
from routes.rutas import rutas
from routes.ruta_auth import route_sharff
from dotenv import load_dotenv

app = Flask(__name__)
app.register_blueprint(routes_auth, url_prefix="/")
app.register_blueprint(rutas, url_prefix="/")
app.register_blueprint(route_sharff, url_prefix="/")

# La conexion para poder trabajar con la base de datos
conexion = MySQL(app)   

def pagina_no_encontrada(error):
    """
    Retorna una pagina de error cuando no se encuentra la pagina
    
    :param error: The error that was raised
    """
    #return "<h1>La pagina que intentas buscar no existe ... </h1>", 404
    return render_template('errors/404.html'), 404


def error_autorizacion(error):
    """
    Retorna una pagina de error al no tener autentificacion
    
    :param error: The error that was raised
    """
    #return "<h1>La pagina que intentas buscar no existe ... </h1>", 404
    return render_template('errors/405.html'), 405



if __name__ == '__main__':
    # Recurre al archivo configuracion y toma el parametro DEBUG = TRUE
    app.config.from_object(config['development'])
    # Registro la funcion pagina_no_encontrada como pagina de error
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(405, error_autorizacion)
    # Inicia el servidor en el puerto 5000
    app.run(port=5000)
