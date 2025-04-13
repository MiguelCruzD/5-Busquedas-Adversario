"""
Modulo para las clases básicas para realizar un jkuego de forma muy simplificada
    
Vamos a usar una orientación funcional en este modulo

"""

from random import shuffle
    
class ModeloJuegoZT2:
    """
    Clase abstracta para juegos de suma cero, por turnos, dos jugadores.
    
    Se asumen que los jugadores son 1 y -1
    """
    
    def inicializa(self):
        """
        Inicializa el estado inicial del juego y el jugador
        que comienza (típicamente el primero)
        
        devuelve: (s0, j) donde s0 es el estado inicial y j el jugador
        """
        # El estado inicial es un tablero vacío
        s0 = ['.' for _ in range(9)]  # Una lista de 9 elementos, todos inicializados a '.'
        
        # El jugador 1 comienza primero
        j = 1  # Jugador 1 comienza
        
        return s0, j
    
    def jugadas_legales(self, s, j):
        """
        Devuelve una lista con las jugadas legales para el jugador j
        en el estado s
        
        """
        jugadas = []
        for i in range(len(s)):
            if s[i] == '.':  # Si la casilla está vacía
                jugadas.append(i)  # Se agrega la casilla como jugada legal
        
        return jugadas    
    
    def transicion(self, s, a, j):
        """
        Devuelve el estado que resulta de realizar la jugada a en el estado s
        para el jugador j
        
        """
        # Crear una copia del estado actual del tablero
        nuevo_estado = s[:]
        
        # Colocar el símbolo del jugador j en la posición indicada por la jugada a
        nuevo_estado[a] = 'X' if j == 1 else 'O'
        
        return nuevo_estado
    
    def terminal(self, s):
        """
        Determina si el juego ha llegado a un estado terminal.
        Un estado terminal puede ser un estado con ganador o empate.
        """
        # Si ya hay un ganador, el juego terminó
        if self.ganancia(s) != 0:
            return True
        
        # Si no hay movimientos legales, también terminó
        if not any(self.jugadas_legales(s, j) for j in [-1, 1]):
            return True
        
        return False
    
    def ganancia(self, s):
        """
        Devuelve la ganancia para el jugador 1 en el estado terminal s.
        Si el jugador 1 gana, devuelve 1, si el jugador -1 gana, devuelve -1, y 0 si es empate.
        """
        # Definir las combinaciones ganadoras (líneas horizontales, verticales y diagonales)
        combinaciones_ganadoras = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columnas
            [0, 4, 8], [2, 4, 6]              # diagonales
        ]
        
        for combinacion in combinaciones_ganadoras:
            # Si hay una línea ganadora con el mismo valor (1 o -1)
            if s[combinacion[0]] == s[combinacion[1]] == s[combinacion[2]] and s[combinacion[0]] != '.':
                return s[combinacion[0]]  # Devuelve 1 o -1 según el jugador ganador
        
        # Si no hay ganador y todos los espacios están llenos, es un empate
        if '.' not in s:
            return 0  # Empate
        
        return None  # Si el juego no ha terminado, devuelve None


def juega_dos_jugadores(juego, jugador1, jugador2):
    """
    Juega un juego de dos jugadores
    
    juego: instancia de ModeloJuegoZT
    jugador1: función que recibe el estado y devuelve la jugada
    jugador2: función que recibe el estado y devuelve la jugada
    
    """
    s, j = juego.inicializa()
    while not juego.terminal(s):
        a = jugador1(juego, s, j) if j == 1 else jugador2(juego, s, j)
        s = juego.transicion(s, a, j)
        j = -j
    return juego.ganancia(s), s


def minimax(juego, estado, jugador):
    """
    Devuelve la mejor jugada para el jugador en el estado
    
    """
    j = jugador
    def max_val(estado, jugador):
        if juego.terminal(estado):
            return j * juego.ganancia(estado)
        v = -1e10
        for a in juego.jugadas_legales(estado, jugador):
            v = max(
                v, 
                min_val(
                    juego.transicion(estado, a, jugador), 
                    -jugador
                )
            )
        return v
    
    def min_val(estado, jugador):
        if juego.terminal(estado):
            return j * juego.ganancia(estado)
        v = 1e10
        for a in juego.jugadas_legales(estado, jugador):
            v = min(
                v, 
                max_val(
                    juego.transicion(estado, a, jugador), 
                    -jugador
                )
            )
        return v
    
    return max(
        juego.jugadas_legales(estado, jugador),
        key=lambda a: min_val(
            juego.transicion(estado, a, jugador), 
            -jugador
            )
        )
    

def alpha_beta(juego, estado, jugador, ordena=None):
    """
    Devuelve la mejor jugada para el jugador en el estado
    
    """
    j = jugador
    def max_val(estado, jugador, alpha, beta):
        if juego.terminal(estado):
            return j * juego.ganancia(estado)
        v = -1e10
        jugadas = list(juego.jugadas_legales(estado, jugador))
        if ordena:
            jugadas = ordena(jugadas)
        else:
            shuffle(jugadas)
        for a in jugadas:
            v = max(
                v, 
                min_val(
                    juego.transicion(estado, a, jugador), 
                    -jugador, 
                    alpha, beta
                )
            )
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    
    def min_val(estado, jugador, alpha, beta):
        if juego.terminal(estado):
            return j * juego.ganancia(estado)
        v = 1e10
        jugadas = list(juego.jugadas_legales(estado, jugador))
        if ordena:
            jugadas = ordena(jugadas)
        else:
            shuffle(jugadas)
        for a in jugadas:
            v = min(
                v, 
                max_val(
                    juego.transicion(estado, a, jugador), 
                    -jugador, 
                    alpha, beta
                )
            )
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    jugadas = list(juego.jugadas_legales(estado, jugador))
    if ordena:
        jugadas = ordena(jugadas)
    else:
        shuffle(jugadas)
    return max(
        jugadas,
        key=lambda a: min_val(
                juego.transicion(estado, a, jugador), 
                -jugador, 
                -1e10, 1e10
            ))