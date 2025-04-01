## Simulación de Cuerpos Celestes

# Descripción
Este proyecto simula el movimiento de cuerpos celestes (como planetas o cometas) en órbitas elípticas, circulares e hiperbólicas, basándose en las leyes de Kepler. Utiliza métodos numéricos (Euler y Runge-Kutta) para resolver ecuaciones diferenciales y visualiza los resultados mediante gráficos estáticos y animaciones interactivas.

## Contenido del proyecto y orden de ejecución
- `metodo_numerico.py`: Clase abstracta para métodos numéricos
- `euler.py`: Implementación del método de Euler
- `runge_kutta.py`: Implementación de Runge-Kutta 4º orden con decoradores para cache y medición de tiempo
- `orbita.py`: Simulación estática de una órbita usando Runge-Kutta
- `planeta.py`: Animación de una órbita con/sin fricción
- `animacion.py`: Comparación de órbitas de tres cuerpos con distintas condiciones iniciales





## 📊 Parámetros Clave

Estos son los principales parámetros que puedes ajustar en las simulaciones:

```python
# Físicos
mu = 1.0       # Constante gravitacional [UA³/año²]
L = 1.0        # Momento angular específico [UA²/año] 
K = 2.0        # Constante de fuerza [UA²/año²]

# Numéricos
h = 0.01       # Paso de integración [radianes]

# Condiciones iniciales
z0 = 1.0       # Inverso de distancia inicial (1/r0) [UA⁻¹]
w0 = -0.1      # Derivada inicial de z (dz/dψ) [UA⁻¹]

# Rango de simulación
psi_start = 0  # Ángulo inicial [rad]
psi_end = 10   # Ángulo final [rad]


