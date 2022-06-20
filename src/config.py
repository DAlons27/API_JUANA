# Configuraciones del proyecto

class DevelopmentConfig():
    # Modo de desarrollo
    DEBUG = True 

    # Credenciales para conectarse a la base de datos
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Yawen123@'
    MYSQL_DB = 'listproduct'
 
config={
    'development': DevelopmentConfig
}

