from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


from routes.auth import routes_auth
from dotenv import load_dotenv
from routes.rutas import rutas


app = Flask(__name__)
app.register_blueprint(routes_auth, url_prefix="/")
app.register_blueprint(rutas, url_prefix="/")

# La conexion para poder trabajar con la base de datos
conexion = MySQL(app)

def pagina_no_encontrada(error):
    """
    It returns a 404 error page
    
    :param error: The error that was raised
    """
    return "<h1>La pagina que intentas buscar no existe ... </h1>", 404


if __name__ == '__main__':
    # Recurre al archivo configuracion y toma el parametro DEBUG = TRUE
    app.config.from_object(config['development'])
    # Manejador de errores, se le pasa como argumento el codigo de respuesta y la funcion
    app.register_error_handler(404, pagina_no_encontrada)
    # Inicia el servidor en el puerto 5000
    app.run(port=5000)
