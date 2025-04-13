from ultimate_tictactoe import UltimateTicTacToe
from minimax import minimax_iterativo

def evalua(estado):
    """
    Evaluación simple de los estados: cuenta las fichas 'X' y 'O' y retorna la diferencia.
    """
    total_x = 0
    total_o = 0
    for subtablero in estado['tablero']:
        for fila in subtablero:
            for celda in fila:
                if celda == 'X':
                    total_x += 1
                elif celda == 'O':
                    total_o += 1
    return total_x - total_o


def mostrar_tablero(estado):
    """
    Muestra el estado actual del tablero en un formato amigable.
    """
    tableros = estado['tablero']
    ganados = estado['ganados']
    print("Estado del juego:")
    for fila in range(3):
        for subfila in range(3):
            linea = ''
            for col in range(3):
                index = fila * 3 + col
                # Se muestran los subtableros
                linea += ' '.join(tableros[index][subfila]) + ' | '
            print(linea[:-2])  # Eliminar la última barra vertical
        print("-" * 30)  # Separador entre subtableros
    print("Ganados:", ganados)
    print("Subtablero actual:", estado['subtablero_actual'])


def obtener_entrada_jugador():
    """
    Función para obtener la entrada del jugador de forma segura.
    La entrada se espera en el formato subtablero,fila,columna.
    """
    while True:
        try:
            entrada = input("Tu jugada (subtablero,fila,columna): ")
            s, f, c = map(int, entrada.strip().split(","))
            if 0 <= s < 9 and 0 <= f < 3 and 0 <= c < 3:
                return s, f, c
            else:
                print("Por favor ingresa valores dentro de los rangos válidos.")
        except ValueError:
            print("Entrada inválida. Asegúrate de usar el formato correcto: subtablero,fila,columna.")


# Inicialización del juego
juego = UltimateTicTacToe()
estado = juego.estado_inicial

# Bucle principal del juego
while not juego.es_terminal(estado):
    mostrar_tablero(estado)
    turno = juego.jugador(estado)

    if turno == 'X':  # Jugador humano
        print(f"Es tu turno, {turno}.")
        accion = obtener_entrada_jugador()
    else:  # Jugador IA (Minimax)
        print("IA pensando...")
        accion = minimax_iterativo(juego, estado, jugador=-1, tiempo=3, evalua=evalua)  # IA juega con 'O'
        print("IA juega:", accion)

    estado = juego.resultado(estado, accion)

mostrar_tablero(estado)

# Resultado final
if juego.gano_tablero_global(estado['ganados'], 'X'):
    print("¡Felicidades! Has ganado.")
elif juego.gano_tablero_global(estado['ganados'], 'O'):
    print("La IA ha ganado.")
else:
    print("El juego ha terminado en empate.")
