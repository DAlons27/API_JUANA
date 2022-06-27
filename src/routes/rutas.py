from flask import Blueprint, jsonify, request
from function_jwt import validate_token
from function_validation import validar_nPedido

rutas = Blueprint("rutas", __name__)

@rutas.route("/mostrarEstado", methods=["GET"])                         # listo
def mostrarEstado():
    """
    Me muestra todos los estados de los pedidos de la base de datos
    """
    from app import conexion
    try:
        # Crea una conexion con la base de datos
        cursor = conexion.connection.cursor()
        # Consulta sql
        sql = "SELECT * FROM productos"
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

@rutas.route('/mostrarEstado/<n_pedido>', methods=['GET'])              # Listo
def mostra_pedido(n_pedido):
    """
    Me muestra el estado del numero de pedido que se le pasa por parametro
    
    :parametro n_pedido: El numero de pedido que es unico
    """
    from app import conexion
    try:
        cursor = conexion.connection.cursor()
        # Consulta sql, el numero de pedido que se le pasa por parametro y se usa el format para que se pueda usar el parametro
        sql = "SELECT * FROM productos WHERE numeroPedido = '{0}' ORDER BY tiempo DESC".format(
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

@rutas.route('/historialPedido/<n_pedido>', methods=['GET'])            # Listo
def historial_pedido(n_pedido):
    """
    Me muestra un historial segun el numero de Pedido que se le pasa por parametro
    :parametro n_pedido: El numero de pedido que es unico
    """
    from app import conexion
   
    cursor = conexion.connection.cursor()
    # Consulta sql, el numero de pedido que se le pasa por parametro y se usa el format para que se pueda usar el parametro
    sql = "SELECT * FROM productos WHERE numeroPedido = '{0}'".format(n_pedido)
    cursor.execute(sql)
    # el fetchone es para que solo me devuelva una fila(la que necesito segun el numero de pedido)
    datos = cursor.fetchall()

    try:
        if len(n_pedido) < 5:
            return jsonify({'mensaje': "Error: formato de numero de pedido incorrecto"})      
        else:
            if len(datos) < 1:
                return jsonify({'mensaje': "Error, numero de pedido no tiene historial."})
            pedidos = []
            for i in datos:
                    # Creating a dictionary with the data from the database.
                pedido = {'numeroGuia': i[0], 'numeroPedido': i[1], 'estado': i[2], 'lugar': i[3], 'quienRecibe': i[4],
                            'motivoDescripcion': i[5], 'fecha': i[6], 'hora': i[7], 'link': i[8], 'observacion': i[9]}
                    # Appending the dictionary `pedido` to the list `pedidos`.
                pedidos.append(pedido)
        return jsonify({'pedidos': pedidos, 'mensaje': "Pedido encontrado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@rutas.route('/eliminarEstado/<n_pedido>', methods=['DELETE'])          # Listo
def eliminar_estado(n_pedido):
    """
    Me elimina el estado del pedido que se le pasa por parametro
    
    :parametro n_guia: El numero de pedido que es unico
    """
    from app import conexion
    try:
        cursor = conexion.connection.cursor()
        # Obtengo los datos del json que se le pasa por parametro y los guardo en una variable
        sql = "DELETE FROM productos WHERE numeroPedido = '{0}'".format(
            n_pedido)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la accion de insercion
        return jsonify({'mensaje': "Estado del Pedido eliminado..."})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})

