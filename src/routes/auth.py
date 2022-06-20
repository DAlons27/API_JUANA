from flask import Blueprint, jsonify, request
from function_jwt import write_token, validate_token

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route("/login", methods=["POST"])
def login():
    """
    Permite que el usuario genere al token para poder acceder a las rutas
    """
    data = request.get_json()
    if data['username'] == "UsuarioSharff":
        return write_token(data=request.get_json())
    else:
        response = jsonify({"message": "User not found"})
        response.status_code = 404
        return response

@routes_auth.route("/verifyToken", methods=["GET"])
def verifyToken():
    """
    Permite que el usuario verifique el token para poder acceder a las rutas
    """
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)
