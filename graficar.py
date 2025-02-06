import matplotlib.pyplot as plt

def plotex(cxs, cys, dxs, dys):
    plt.xlabel('x', fontsize=20)
    plt.ylabel('f(x)', fontsize=20)
    plt.plot(cxs, cys, 'r-', label='one function')  # Línea roja
    plt.plot(dxs, dys, 'b--', label='other function')  # Línea azul punteada
    plt.legend()
    plt.show()
#la relampara






# simona

# Datos
cxs = [0.1 * i for i in range(60)]
cys = [x**2 for x in cxs]
dxs = [i for i in range(7)]
dys = [x - 0.5 for x in dxs]

# Llamada a la función para graficar
plotex(cxs, cys, dxs, dys)
