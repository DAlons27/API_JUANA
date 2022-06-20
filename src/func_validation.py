def validar_nPedido(numeroPedido: str) -> bool:
    """
        Funcion que valida la cantidad de caracteres del numero de pedido
        """
    return len(numeroPedido) == 16
