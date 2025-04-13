from random import shuffle
from time import time


def estado_hashable(estado):
    # Primero recorrer subtableros, luego las filas dentro de cada subtablero
    tablero_hashable = tuple(
        tuple(
            tuple(celda) for celda in fila
        ) for subtablero in estado['tablero'] for fila in subtablero
    )
    return tablero_hashable


def negamax(
    juego, estado, jugador,
    alpha=-1e10, beta=1e10, ordena=None, 
    d=None, evalua=None,
    transp={}, traza=[]
    ):
    if d != None and evalua == None:
        raise ValueError("Se necesita evalua si d no es None")
    if type(ordena) != type(None) and type(ordena) != type(lambda x: x):
        raise ValueError("ordena debe ser una función")
    if type(evalua) != type(None) and type(evalua) != type(lambda x: x):
        raise ValueError("evalua debe ser una función")
    if type(transp) != dict:
        raise ValueError("transp debe ser un diccionario")
    if type(traza) != list: 
        raise ValueError("traza debe ser una lista")

    if juego.es_terminal(estado):
        return [], juego.utilidad(estado, 'X') if jugador == 1 else juego.utilidad(estado, 'O')
    if d == 0:
        return [], jugador * evalua(estado)
    
    # Convertir el estado en una representación hashable para usarlo en las transposiciones
    estado_hash = estado_hashable(estado)
    
    if d != None and estado_hash in transp and transp[estado_hash][1] >= d:
        return [], transp[estado_hash][0]
    
    v = -1e10
    jugadas = list(juego.acciones(estado))
    if ordena != None:
        jugadas = ordena(jugadas, jugador)
    else:
        shuffle(jugadas)
    if traza:
        a_pref = traza.pop(0)
        if a_pref in jugadas:
            jugadas = [a_pref] + [a for a in jugadas if a != a_pref]
    for a in jugadas:
        traza_actual, v2 = negamax(
            juego, juego.resultado(estado, a), -jugador, 
            -beta, -alpha, ordena, d if d == None else d - 1, 
            evalua, transp, traza
        )
        v2 = -v2
        if v2 > v:
            v = v2
            mejor = a
            mejores = traza_actual[:]
        if v >= beta:
            break
        if v > alpha:
            alpha = v
    transp[estado_hash] = (v, d)
    return [mejor] + mejores, v 


def jugador_negamax(
    juego, estado, jugador, ordena=None, d=None, evalua=None
    ):
    traza, _ = negamax(
        juego=juego, estado=estado, jugador=jugador, 
        alpha=-1e10, beta=1e10, ordena=ordena, d=d, 
        evalua=evalua, transp={}, traza=[])
    return traza[0]


def minimax_iterativo(
    juego, estado, jugador, tiempo=10,
    ordena=None, d=None, evalua=None,
    ):  
    t0 = time()
    d, traza = 2, []
    while time() - t0 < tiempo/2:
        traza, v = negamax(
            juego=juego, estado=estado, jugador=jugador,  
            alpha=-1e10, beta=1e10, ordena=ordena, d=d, evalua=evalua, 
            transp={}, traza=traza
        )
        d += 1
    return traza[0]