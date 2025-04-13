from juegos_simplificado import ModeloJuegoZT2
import copy

VACIO = '.'
JUGADORES = ['X', 'O']
TAM = 3  # 3x3

class UltimateTicTacToe(ModeloJuegoZT2):
    def __init__(self):
        super().__init__()
        tablero = [[[VACIO for _ in range(TAM)] for _ in range(TAM)] for _ in range(TAM * TAM)]
        self.estado_inicial = {
            'tablero': tablero,
            'ganados': [VACIO for _ in range(TAM * TAM)],  # Quién ganó cada subtablero
            'turno': 'X',
            'subtablero_actual': None  # Si None, puede jugar en cualquier subtablero
        }

    def jugador(self, estado):
        return estado['turno']

    def acciones(self, estado):
        acciones = []
        for i in range(9):
            if estado['subtablero_actual'] is not None and i != estado['subtablero_actual']:
                continue
            if estado['ganados'][i] != VACIO:
                continue  # subtablero ya ganado
            for fila in range(TAM):
                for col in range(TAM):
                    if estado['tablero'][i][fila][col] == VACIO:
                        acciones.append((i, fila, col))
        return acciones

    def resultado(self, estado, accion):
        i, fila, col = accion
        nuevo_estado = copy.deepcopy(estado)
        nuevo_estado['tablero'][i][fila][col] = estado['turno']

        # Verificar si se ganó el subtablero
        if self.gano(nuevo_estado['tablero'][i], estado['turno']):
            nuevo_estado['ganados'][i] = estado['turno']

        # Cambiar turno
        nuevo_estado['turno'] = 'O' if estado['turno'] == 'X' else 'X'

        # Subtablero siguiente (depende de la jugada que hiciste)
        siguiente_sub = fila * TAM + col
        if nuevo_estado['ganados'][siguiente_sub] != VACIO:
            nuevo_estado['subtablero_actual'] = None
        else:
            nuevo_estado['subtablero_actual'] = siguiente_sub

        return nuevo_estado

    def es_terminal(self, estado):
        return self.gano_tablero_global(estado['ganados'], 'X') or \
               self.gano_tablero_global(estado['ganados'], 'O') or \
               all(x != VACIO for x in estado['ganados'])

    def utilidad(self, estado, jugador):
        if self.gano_tablero_global(estado['ganados'], jugador):
            return 1
        elif self.gano_tablero_global(estado['ganados'], self.oponente(jugador)):
            return -1
        else:
            return 0

    def oponente(self, jugador):
        return 'O' if jugador == 'X' else 'X'

    def gano(self, tablero, jugador):
        for i in range(TAM):
            if all(tablero[i][j] == jugador for j in range(TAM)):
                return True
            if all(tablero[j][i] == jugador for j in range(TAM)):
                return True
        if all(tablero[i][i] == jugador for i in range(TAM)):
            return True
        if all(tablero[i][TAM-1-i] == jugador for i in range(TAM)):
            return True
        return False

    def gano_tablero_global(self, ganados, jugador):
        matriz = [[ganados[i * TAM + j] for j in range(TAM)] for i in range(TAM)]
        return self.gano(matriz, jugador)