from flask import Blueprint, jsonify, request
from function_jwt import write_token, validate_token

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data['username'] == "UsuarioSharff":
        return write_token(data=request.get_json())
    else:
        response = jsonify({"message": "User not found"})
        response.status_code = 404
        return response

 # Verificador de token
@routes_auth.route("/verifyToken", methods=["GET"])
def verifyToken():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)
