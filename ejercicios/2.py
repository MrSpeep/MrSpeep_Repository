import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from abc import ABC, abstractmethod
from functools import lru_cache
import time

# Clase abstracta para cuerpos celestes
class CuerpoCeleste(ABC):
    def __init__(self, masa, x, y, vx, vy):
        self._masa = masa
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy
        self.trayectoria = []  # Lista para almacenar la trayectoria

    @property
    def masa(self):
        return self._masa

    @property
    def posicion(self):
        return self._x, self._y

    @property
    def velocidad(self):
        return self._vx, self._vy

    @abstractmethod
    def actualizar_posicion(self):
        pass

    def agregar_trayectoria(self):
        # Almacenar la posición actual de la partícula
        self.trayectoria.append((self._x, self._y))

# Clase derivada para un planeta (puede ser extendida para otros cuerpos celestes)
class Planeta(CuerpoCeleste):
    def __init__(self, masa, x, y, vx, vy, epsilon):
        super().__init__(masa, x, y, vx, vy)
        self.epsilon = epsilon  # Excentricidad

    @lru_cache(None)  # Cache para almacenar resultados de la órbita
    def calcular_orbita(self, alpha, psi):
        """
        Calcula la órbita según la ley de Kepler y la excentricidad epsilon.
        """
        denominador = 1 + self.epsilon * math.cos(psi)
        if abs(denominador) < 1e-6:
            return None
        return alpha / denominador

    def actualizar_posicion(self, alpha, psi):
        # Actualiza la posición del planeta
        r = self.calcular_orbita(alpha, psi)
        if r is not None:
            self._x = r * math.cos(psi)
            self._y = r * math.sin(psi)
        self.agregar_trayectoria()  # Agregar la nueva posición a la trayectoria

# Clase derivada para un asteroide (ejemplo de herencia múltiple)
class Asteroide(Planeta):
    def __init__(self, masa, x, y, vx, vy, epsilon, velocidad_inicial):
        super().__init__(masa, x, y, vx, vy, epsilon)
        self.velocidad_inicial = velocidad_inicial  # Velocidad inicial del asteroide

    def actualizar_posicion(self, alpha, psi):
        # Modificamos ligeramente la velocidad en la actualización
        velocidad_ajustada = self.velocidad_inicial * (1 + 0.1 * math.sin(psi))
        r = self.calcular_orbita(alpha, psi)
        if r is not None:
            self._x = r * math.cos(psi) * velocidad_ajustada
            self._y = r * math.sin(psi) * velocidad_ajustada
        self.agregar_trayectoria()

# Decorador para medir el tiempo de ejecución
def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {end_time - start_time:.4f} segundos")
        return result
    return wrapper

# Función para animación
@timing
def animar_orbitas(planetas, alpha, psi_vals, velocidad_factor=1):
    fig, ax = plt.subplots(figsize=(7, 7))

    def update(num):
        ax.clear()
        # Aumentamos el valor de psi para acelerar el avance de las partículas
        velocidad_psi = psi_vals[num] * velocidad_factor  # Esto hace que las partículas se muevan más rápido
        for planeta in planetas:
            planeta.actualizar_posicion(alpha, velocidad_psi)

            # Graficar la trayectoria de la partícula (todas las posiciones anteriores)
            trayectoria_x, trayectoria_y = zip(*planeta.trayectoria)  # Extraer las posiciones
            ax.plot(trayectoria_x, trayectoria_y, linestyle='-', color='gray', alpha=0.6)  # Trayectoria

            # Graficar la posición actual de la partícula
            ax.plot(planeta.posicion[0], planeta.posicion[1], 'bo')

        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, linestyle="--", linewidth=0.5)

    ani = animation.FuncAnimation(fig, update, frames=len(psi_vals), interval=30)  # Menor intervalo
    plt.show()

# Parámetros de la órbita
alpha = 1
epsilon_vals = [0, 0.5, 1]  # Diferentes excentricidades

# Crear planetas y asteroides
planetas = [Planeta(5.97e24, 1, 0, 0, 0, epsilon) for epsilon in epsilon_vals]
asteroides = [Asteroide(1.5e12, 0.5, 0, 0, 0, 0.3, 1.5) for _ in range(3)]  # Asteroides con diferente velocidad

# Generar valores de psi para la simulación con un incremento pequeño
psi_vals = [i * 0.001 for i in range(0, int(2 * math.pi * 200))]  # Incremento más pequeño para más suavidad

# Ejecutar la animación con un factor de velocidad mayor
animar_orbitas(planetas + asteroides, alpha, psi_vals, velocidad_factor=50)  # Aumentamos la velocidad de las partículas
