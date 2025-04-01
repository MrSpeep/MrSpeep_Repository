import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from runge_kutta import RungeKutta
from euler import Euler

# Configuración de constantes y parámetros
CONFIG = {
    "mu": 1.0,          # Constante gravitacional
    "K": 2.0,           # Constante de fuerza
    "h": 0.01,          # Paso de integración
    "psi_range": (0, 15), # Rango angular [start, end]
    "planets": [
        {"nombre": "Circular", "color": "blue", "z0": 1.0, "w0": 0.0, "L": 1.0},
        {"nombre": "Elíptica", "color": "green", "z0": 1.0, "w0": -0.1, "L": 1.0},
        {"nombre": "Hipérbola", "color": "orange", "z0": 0.5, "w0": -0.6, "L": 1.0},
    ]
}

def create_orbital_system(L):
    """Crea el sistema de ecuaciones diferenciales para un momento angular L dado"""
    def system(psi, y):
        z, w = y
        dz_dpsi = w
        dw_dpsi = -z + (CONFIG["mu"] * CONFIG["K"]) / (L ** 2)
        return [dz_dpsi, dw_dpsi]
    return system

def calculate_orbit(method, system, y0):
    """Calcula la órbita usando el método numérico especificado"""
    solver = method(system, CONFIG["h"])
    return solver.solve(CONFIG["psi_range"], y0)

def convert_to_cartesian(psi_values, y_values):
    """Convierte los resultados a coordenadas cartesianas"""
    z_vals = [y[0] for y in y_values]
    r_vals = [1/z if abs(z) > 1e-8 else 1e8 for z in z_vals]  # Manejo seguro de división por cero
    x_vals = [r * math.cos(psi) for r, psi in zip(r_vals, psi_values)]
    y_vals = [r * math.sin(psi) for r, psi in zip(r_vals, psi_values)]
    return x_vals, y_vals

# Pre-cálculo de todas las órbitas
for planet in CONFIG["planets"]:
    system = create_orbital_system(planet["L"])
    # Cambiar entre Euler y Runge-Kutta según sea necesario
    psi_values, y_values = calculate_orbit(Euler, system, [planet["z0"], planet["w0"]])
    planet["x"], planet["y"] = convert_to_cartesian(psi_values, y_values)
    planet["frames"] = len(psi_values)

# Configuración de la figura
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title("Simulación de Órbitas Planetarias", pad=20)
ax.set_xlabel("Coordenada x (UA)", labelpad=10)
ax.set_ylabel("Coordenada y (UA)", labelpad=10)
ax.grid(alpha=0.3)
ax.set_aspect("equal")

# Ajuste automático de límites
all_coords = [coord for planet in CONFIG["planets"] for coord in planet["x"] + planet["y"]]
max_range = max(abs(min(all_coords)), abs(max(all_coords))) * 1.1
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)

# Cuerpo central
ax.plot(0, 0, 'ro', markersize=10, label="Estrella central")

# Elementos animados
lines = []
points = []
for planet in CONFIG["planets"]:
    line, = ax.plot([], [], lw=1.5, color=planet["color"], label=planet["nombre"])
    point, = ax.plot([], [], 'o', color=planet["color"], markersize=8)
    lines.append(line)
    points.append(point)

# Función de inicialización
def init():
    for line, point in zip(lines, points):
        line.set_data([], [])
        point.set_data([], [])
    return lines + points

# Función de actualización optimizada
def update(frame):
    for i, planet in enumerate(CONFIG["planets"]):
        # Usamos el mínimo entre frame y la longitud de los datos
        effective_frame = min(frame, len(planet["x"]) - 1)
        if effective_frame > 0:
            lines[i].set_data(planet["x"][:effective_frame], planet["y"][:effective_frame])
            points[i].set_data([planet["x"][effective_frame]], [planet["y"][effective_frame]])
    return lines + points

# Crear animación con parámetros optimizados
total_frames = min(800, max(planet["frames"] for planet in CONFIG["planets"]))
ani = FuncAnimation(
    fig, update, frames=total_frames,
    init_func=init, blit=True, interval=40, repeat=True
)

plt.legend(loc='upper right')
plt.tight_layout()
plt.show()