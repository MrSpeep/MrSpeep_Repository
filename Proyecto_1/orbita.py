import math
import matplotlib.pyplot as plt
from runge_kutta import RungeKutta  # Asegúrate de tener tu implementación
from euler import Euler             # Opcional para comparación

# Parámetros físicos (organizados en diccionario para claridad)
params = {
    'mu': 1,          # Constante gravitacional
    'L': 1,           # Momento angular
    'K': 2,           # Constante de fuerza
    'h': 0.01,        # Paso de integración
    'psi_range': (0, 10),  # Rango angular [start, end]
    'y0': [1, -0.1]   # Condiciones iniciales [z0, w0]
}

# Sistema de ecuaciones diferenciales (versión más legible)
def orbital_system(psi, y):
    z, w = y
    dz_dpsi = w
    dw_dpsi = -z + (params['mu'] * params['K']) / (params['L']**2)
    return [dz_dpsi, dw_dpsi]

# Resolución con Runge-Kutta y euler
# Resolución con ambos métodos
rk_solver = RungeKutta(orbital_system, params['h'])
euler_solver = Euler(orbital_system, params['h'])  # <- Así se agrega Euler

# Calculamos ambas trayectorias
psi_rk, y_rk = rk_solver.solve(params['psi_range'], params['y0'])
psi_euler, y_euler = euler_solver.solve(params['psi_range'], params['y0'])

# Procesamiento para Runge-Kutta
r_rk = [1/z if abs(z) > 1e-8 else 1e8 for z in [y[0] for y in y_rk]]
x_rk = [r * math.cos(psi) for r, psi in zip(r_rk, psi_rk)]
y_rk = [r * math.sin(psi) for r, psi in zip(r_rk, psi_rk)]

# Procesamiento para Euler (misma lógica)
r_euler = [1/z if abs(z) > 1e-8 else 1e8 for z in [y[0] for y in y_euler]]
x_euler = [r * math.cos(psi) for r, psi in zip(r_euler, psi_euler)]
y_euler = [r * math.sin(psi) for r, psi in zip(r_euler, psi_euler)]

plt.figure(figsize=(10, 8))

# Plot Runge-Kutta
plt.plot(x_rk, y_rk, color='blue', linewidth=1.5, label='Runge-Kutta (4to orden)')

# Plot Euler
plt.plot(x_euler, y_euler, color='green', linestyle='--', linewidth=1, label='Euler')

# Cuerpo central
plt.scatter(0, 0, color='red', s=100, label='Cuerpo central')

plt.title("Comparación de Métodos Numéricos")
plt.xlabel("Coordenada x")
plt.ylabel("Coordenada y")
plt.legend()
plt.grid(alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()