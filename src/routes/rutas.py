from flask import Blueprint, jsonify, request
from function_jwt import validate_token
from func_validation import validar_nPedido

rutas = Blueprint("rutas", __name__)

@rutas.before_request
def verify_token_middleware():
    """
    Token de autenticacion para poder acceder a las rutas 
    """
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=False)

 
@rutas.route("/mostrarEstado", methods=["GET"])
def mostrarEstado():
    """
    Me muestra todos los estados de los pedidos de la base de datos
    """
    from app import conexion
    try:
        # Crea una conexion con la base de datos
        cursor = conexion.connection.cursor()
        # Consulta sql
        sql = "SELECT * FROM products"
        # Ejecuto la consulta
        cursor.execute(sql)
        # Obtengo los datos
        estado = cursor.fetchall()
        pedidos = []
        for i in estado:
            # Creating a dictionary with the data from the database.
            pedido = {'numeroGuia': i[0], 'numeroPedido': i[1], 'estado': i[2], 'lugar': i[3], 'quienRecibe': i[4],
                      'motivoDescripcion': i[5], 'fecha': i[6], 'hora': i[7], 'link': i[8], 'observacion': i[9]}
            # Appending the dictionary `pedido` to the list `pedidos`.
            pedidos.append(pedido)
        # Returning a JSON object with the key `pedidos` and the value `pedidos`.
        return jsonify({'pedidos': pedidos})

    except Exception as ex:
        # Returning a JSON object with the key `mensaje` and the value `Error`.
        return jsonify({'mensaje': "Error"})

@rutas.route('/mostrarEstado/<n_pedido>', methods=['GET'])
def mostra_pedido(n_pedido):
    """
    Me muestra el estado del numero de pedido que se le pasa por parametro
    
    :parametro n_guia: El numero de pedido que es unico
    """
    from app import conexion
    try:
        cursor = conexion.connection.cursor()
        # Consulta sql, el numero de pedido que se le pasa por parametro y se usa el format para que se pueda usar el parametro
        sql = "SELECT * FROM products WHERE numeroPedido = '{0}'".format(
            n_pedido)
        cursor.execute(sql)
        # el fetchone es para que solo me devuelva una fila(la que necesito segun el numero de pedido)
        datos = cursor.fetchone()
        # Creando un diccionario con los datos de la base de datos
        if datos != None:
            pedido = {'numeroGuia': datos[0], 'numeroPedido': datos[1], 'estado': datos[2], 'lugar': datos[3], 'quienRecibe': datos[4],
                      'motivoDescripcion': datos[5], 'fecha': datos[6], 'hora': datos[7], 'link': datos[8], 'observacion': datos[9]}
            return jsonify({'pedidos': pedido, 'mensaje': "Pedido encontrado."})
        else:
            return jsonify({'mensaje': "Pedido no encontrado."})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@rutas.route('/historialPedido/<n_pedido>', methods=['GET'])
def historial_pedido(n_pedido):
    """
    Me muestra un historial segun el numero de Pedido que se le pasa por parametro
    """
    from app import conexion
    try:
        cursor = conexion.connection.cursor()
        # Consulta sql, el numero de pedido que se le pasa por parametro y se usa el format para que se pueda usar el parametro
        sql = "SELECT * FROM products WHERE numeroPedido = '{0}'".format(
            n_pedido)
        cursor.execute(sql)
        # el fetchone es para que solo me devuelva una fila(la que necesito segun el numero de pedido)
        datos = cursor.fetchall()
        if datos != None:
            pedido = {'numeroGuia': datos[0], 'numeroPedido': datos[1], 'estado': datos[2], 'lugar': datos[3], 'quienRecibe': datos[4],
                      'motivoDescripcion': datos[5], 'fecha': datos[6], 'hora': datos[7], 'link': datos[8], 'observacion': datos[9]}
            return jsonify({'pedidos': pedido, 'mensaje': "Pedido encontrado."})
        else:
            return jsonify({'mensaje': "Pedido no encontrado."})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@rutas.route('/trasmitirEstado', methods=['POST'])
def trasmitir_estado():
    """
    Permite el registro de informacion en la base de datos por parte de Sharff
    """
    from app import conexion
    # Valido que cumpla con tener 16 caracteres el numero de pedido
    if (validar_nPedido(request.json['numeroPedido'])):
        try:
            cursor = conexion.connection.cursor()
            # Obtengo los datos del json que se le pasa por parametro y los guardo en una variable
            sql = "INSERT INTO products (numeroGuia, numeroPedido, estado, lugar, quienRecibe, motivoDescripcion, fecha, hora, link, observacion) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(
                request.json['numeroGuia'], request.json['numeroPedido'], request.json['estado'], request.json['lugar'], request.json['quienRecibe'], request.json['motivoDescripcion'], request.json['fecha'], request.json['hora'], request.json['link'], request.json['observacion'])
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la accion de insercion
            return jsonify({'mensaje': "Se registró correctamente."})
        except Exception as ex:
            return jsonify({'mensaje': "Error"})
    else:
        return jsonify({'mensaje': "No se pudo registrar."})

@rutas.route('/actualizarEstado/<n_pedido>', methods=['PUT'])
def actualizar_estado(n_pedido):
    """
    Me actualiza el estado del pedido en la base de datos
    
    :parametro n_pedido: El numero de pedido que es unico
    """
    from app import conexion
    try:
        cursor = conexion.connection.cursor()
        # Obtengo los datos del json que se le pasa por parametro y los guardo en una variable
        sql = "UPDATE products SET numeroGuia = '{0}', estado = '{1}', lugar = '{3}', quienRecibe = '{4}', motivoDescripcion = '{5}', fecha = '{6}', hora = '{7}', link = '{8}', observacion = '{9}' WHERE numeroPedido = '{2}'".format(
            request.json['numeroGuia'], request.json['estado'], request.json['lugar'], request.json['quienRecibe'], request.json['motivoDescripcion'], request.json['fecha'], request.json['hora'], request.json['link'], request.json['observacion'], n_pedido)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la accion de insercion
        return jsonify({'mensaje': "Estado del Pedido actualizado..."})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@rutas.route('/eliminarEstado/<n_pedido>', methods=['DELETE'])
def eliminar_estado(n_pedido):
    """
    Me elimina el estado del pedido que se le pasa por parametro
    
    :parametro n_guia: El numero de pedido que es unico
    """
    from app import conexion
    try:
        cursor = conexion.connection.cursor()
        # Obtengo los datos del json que se le pasa por parametro y los guardo en una variable
        sql = "DELETE FROM products WHERE numeroPedido = '{0}'".format(
            n_pedido)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la accion de insercion
        return jsonify({'mensaje': "Estado del Pedido eliminado..."})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})
