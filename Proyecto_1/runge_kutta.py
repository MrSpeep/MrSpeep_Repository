""""En el sigiente codigo orientado a objetos (leyes de Kepler) implementaremos encapsulamiento, decoradores
    un método numerico (Runge-kutta) para determinar las orbitas de un sistema de dos cuerpos"""
from metodo_numerico import MetodoNumerico
import time

# Decoradores
def cache_results(func):
    cache = {}
    def wrapper(*args):
        # Convertir solo las listas o tuplas en tuplas, dejando los demás tipos intactos
        args_tuple = tuple(
            tuple(arg) if isinstance(arg, list) else arg for arg in args
        )
        if args_tuple in cache:
            return cache[args_tuple]
        result = func(*args)
        cache[args_tuple] = result
        return result
    return wrapper

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {end_time - start_time:.4f} segundos")
        return result
    return wrapper

class RungeKutta(MetodoNumerico):
    def __init__(self, system, h):
        self.system = system
        self._h = h

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        if value <= 0:
            raise ValueError("El paso debe ser positivo.")
        self._h = value

    @timing  # Decorador de Timing
    @cache_results  # Decorador de Caching
    def step(self, t, y, h=None):
        if h is None:
            h = self._h
        k1 = self.system(t, y)
        k2 = self.system(t + h/2, [y[i] + h/2 * k1[i] for i in range(len(y))])
        k3 = self.system(t + h/2, [y[i] + h/2 * k2[i] for i in range(len(y))])
        k4 = self.system(t + h, [y[i] + h * k3[i] for i in range(len(y))])
        return [y[i] + (h/6)*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(len(y))]

    def solve(self, t_span, y0):
        t_start, t_end = t_span
        num_steps = int((t_end - t_start) / self._h) + 1
        t_values = [t_start + i * self._h for i in range(num_steps)]
        y_values = [y0]
        y = y0[:]
        for i in range(1, num_steps):
            if t_values[i] > t_end:
                h_last = t_end - t_values[i-1]
                y = self.step(t_values[i-1], y, h_last)
                t_values[i] = t_end
            else:
                y = self.step(t_values[i-1], y)
            y_values.append(y[:])
        return t_values, y_values
