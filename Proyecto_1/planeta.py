import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from runge_kutta import RungeKutta  # Asegúrate de tener este archivo

# Parámetros físicos
mu = 1
L = 1
K = 2
h = 0.01
psi_start = 0
psi_end = 10
z0 = 1
w0 = -0.1
friccion = 0.05  # Cambia a 0 si no quieres fricción

# Definir el sistema de ecuaciones
def system(psi, y):
    z, w = y
    dz_dpsi = w
    dw_dpsi = -z + (mu * K) / (L**2) - friccion * w
    return [dz_dpsi, dw_dpsi]

# Resolver con Runge-Kutta
rk = RungeKutta(system, h)
t_span = (psi_start, psi_end)
y0 = [z0, w0]
psi_values, y_values = rk.solve(t_span, y0)

# Convertir a coordenadas cartesianas
z_values = [y[0] for y in y_values]
r_values = [1 / z if z != 0 else float('inf') for z in z_values]
x_values = [r * math.cos(psi) for r, psi in zip(r_values, psi_values)]
y_cartesian = [r * math.sin(psi) for r, psi in zip(r_values, psi_values)]

# Preparar figura
fig, ax = plt.subplots(figsize=(6, 6))
max_range = max(max(map(abs, x_values)), max(map(abs, y_cartesian))) * 1.1
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_title("Animación de la órbita")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid()
ax.set_aspect("equal")

# Elementos de la animación
line, = ax.plot([], [], lw=2, label="Trayectoria", color="blue")
point, = ax.plot([], [], 'bo', label="Cuerpo en movimiento")
center, = ax.plot(0, 0, 'ro', label="Cuerpo central")
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=10, verticalalignment='top')

# Inicialización
def init():
    line.set_data([], [])
    point.set_data([], [])
    time_text.set_text('')
    return line, point, time_text

# Función de actualización por frame
def update(frame):
    if frame >= len(x_values):
        frame = len(x_values) - 1
    line.set_data(x_values[:frame], y_cartesian[:frame])
    point.set_data([x_values[frame]], [y_cartesian[frame]])  # CORREGIDO
    time_text.set_text(f"ψ (tiempo): {psi_values[frame]:.2f}")
    return line, point, time_text

# Crear la animación
ani = FuncAnimation(
    fig, update, frames=len(x_values),
    init_func=init, blit=True, interval=20
)

plt.legend()
plt.show()
