import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parámetros del sistema
g_0 = 9.81   # Aceleración gravitacional en la superficie de la Tierra (m/s^2)
L = 1.0     # Longitud del péndulo (m)
theta_0 = np.radians(30)  # Ángulo inicial (en radianes)
omega0 = 0  # Velocidad angular inicial (m/s)
epsilon = 0.01  # Factor que ajusta la variación de la gravedad con la distancia

# Función que modela la gravedad variable
def gravity(r):
    return g_0 / (1 + epsilon * r)**2

# Ecuación diferencial para el movimiento del péndulo en un campo gravitacional no uniforme
def pendulum_eq(y, t, L, g_0, epsilon):
    theta, omega = y
    r = L  # Distancia del centro (constantemente L en este modelo)
    g = gravity(r)  # Gravedad en función de r
    dydt = [omega, - (g / L) * np.sin(theta)]  # Ecuación de movimiento
    return dydt

# Condiciones iniciales
y0 = [theta_0, omega0]

# Tiempo de simulación
t = np.linspace(0, 10, 500)  # 10 segundos de simulación

# Resolver la ecuación diferencial
sol = odeint(pendulum_eq, y0, t, args=(L, g_0, epsilon))

# Extraer la solución
theta = sol[:, 0]  # Ángulo
omega = sol[:, 1]  # Velocidad angular

# Graficar el movimiento del péndulo
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, theta, label=r'$\theta(t)$')
plt.title('Movimiento del Péndulo en un Campo Gravitacional No Uniforme')
plt.xlabel('Tiempo (s)')
plt.ylabel('Ángulo (rad)')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, omega, label=r'$\omega(t)$', color='r')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad Angular (rad/s)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()