import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from runge_kutta import RungeKutta  # Asegúrate de tener este archivo en el mismo directorio
from euler import Euler
# Constantes físicas
mu = 1
K = 2
h = 0.01
psi_start = 0
psi_end = 15

# Tres planetas con distintos tipos de órbita
planetas = [
    {"nombre": "Circular",   "color": "blue",   "z0": 1.0, "w0":  0.0, "L": 1.0},
    {"nombre": "Elíptica",   "color": "green",  "z0": 1.0, "w0": -0.1, "L": 1.0},
    {"nombre": "Hipérbola",  "color": "orange", "z0": 0.5, "w0": -0.6, "L": 1.0},
]

# Resolver órbita para cada planeta
for planeta in planetas:
    L = planeta["L"]

    def system(psi, y):
        z, w = y
        dz_dpsi = w
        dw_dpsi = -z + (mu * K) / (L ** 2)
        return [dz_dpsi, dw_dpsi]

    #rk = RungeKutta(system, h)
    euler = Euler(system, h)
    t_span = (psi_start, psi_end)
    y0 = [planeta["z0"], planeta["w0"]]
    #psi_values, y_values = rk.solve(t_span, y0)
    psi_values, y_values = euler.solve(t_span, y0)

    z_vals = [y[0] for y in y_values]
    r_vals = [1 / z if z != 0 else float("inf") for z in z_vals]
    x_vals = [r * math.cos(psi) for r, psi in zip(r_vals, psi_values)]
    y_vals = [r * math.sin(psi) for r, psi in zip(r_vals, psi_values)]

    planeta["x"] = x_vals
    planeta["y"] = y_vals

# Crear la figura
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_title("Órbitas de tres planetas")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid()
ax.set_aspect("equal")
ax.plot(0, 0, 'ro', label="Cuerpo central")

# Ajustar límites
all_x = sum([p["x"] for p in planetas], [])
all_y = sum([p["y"] for p in planetas], [])
max_range = max(max(map(abs, all_x)), max(map(abs, all_y))) * 1.1
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)

# Elementos animados
lines = []
points = []
for planeta in planetas:
    line, = ax.plot([], [], lw=1.5, color=planeta["color"], label=planeta["nombre"])
    point, = ax.plot([], [], 'o', color=planeta["color"])
    lines.append(line)
    points.append(point)

# Inicializar animación
def init():
    for line, point in zip(lines, points):
        line.set_data([], [])
        point.set_data([], [])
    return lines + points

# Actualización por frame (con corrección de IndexError)
def update(frame):
    for i, planeta in enumerate(planetas):
        if frame < len(planeta["x"]) and frame > 0:
            x = planeta["x"][:frame]
            y = planeta["y"][:frame]
            lines[i].set_data(x, y)
            points[i].set_data([x[-1]], [y[-1]])
        elif frame == 0:
            lines[i].set_data([], [])
            points[i].set_data([], [])
    return lines + points

# Crear la animación
ani = FuncAnimation(
    fig, update, frames=800,
    init_func=init, blit=True, interval=20, repeat=False
)

plt.legend()
plt.show()