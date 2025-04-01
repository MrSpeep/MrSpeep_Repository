import math
import matplotlib.pyplot as plt
from runge_kutta import RungeKutta  # Asegúrate de tener tu implementación de Runge-Kutta
from euler import Euler
# Parámetros físicos
mu = 1  # Constante gravitacional
L = 1   # Momento angular específico
K = 2   # Constante de fuerza inversa al cuadrado
h = 0.01  # Paso de integración
psi_start = 0  # Ángulo inicial
psi_end = 10   # Ángulo final
z0 = 1   # Condición inicial: z(0) = 1/r(0)
w0 = -0.1  # Condición inicial: dz/dψ(0)

# Definir el sistema de ecuaciones diferenciales
def system(psi, y):
    z, w = y
    dz_dpsi = w
    dw_dpsi = -z + (mu * K) / (L**2)
    return [dz_dpsi, dw_dpsi]

# Crear una instancia de RungeKutta y resolver
#euler = Euler(system, h)
rk=RungeKutta(system, h)
t_span = (psi_start, psi_end)
y0 = [z0, w0]
#psi_values, y_values = euler.solve(t_span, y0)
psi_values, y_values = rk.solve(t_span, y0)
# Extraer soluciones
z_values = [y[0] for y in y_values]

# Convertir de z a r (r = 1/z)
r_values = [1 / z if z != 0 else float('inf') for z in z_values]

# Convertir ángulos psi a coordenadas cartesianas sin NumPy
x_values = [r * math.cos(psi) for r, psi in zip(r_values, psi_values)]
y_values = [r * math.sin(psi) for r, psi in zip(r_values, psi_values)]

# Graficar la órbita en coordenadas cartesianas
plt.figure(figsize=(8, 8))
plt.plot(x_values, y_values, label="Órbita del cuerpo", color="blue")
plt.scatter(0, 0, color="red", marker="o", label="Cuerpo central")  # Representa el foco
plt.xlabel("x")
plt.ylabel("y")
plt.title("Órbita del cuerpo en coordenadas cartesianas")
plt.legend()
plt.grid()
plt.axis("equal")  # Mantiene la escala 1:1 en los ejes
plt.show()