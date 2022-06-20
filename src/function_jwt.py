from jwt import encode, decode
from jwt import exceptions
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify


def expire_date(days: int):
    """
    Calcula la fecha de expiracion del token
    :param days: Numero de dias que dura el token
    :return: Fecha de expiracion del token
    """
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date


def write_token(data: dict):
    """
    Escribe el token segun la configuracion de la aplicacion
    :param data: Diccionario con los datos del usuario
    :return: Token
    """
    token = encode(payload={**data, "exp": expire_date(2)},
                   key=getenv("SECRET"), algorithm="HS256")
    return token.encode("UTF-8")


def validate_token(token, output=False):
    """
    Valida el token
    :param token: Token
    :param output: True si se quiere imprimir el token, False si no
    :return: True si el token es valido, False si no
    """
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"mensaje": "Token invalido"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"mensaje": "Token expirado"})
        response.status_code = 401
        return response
