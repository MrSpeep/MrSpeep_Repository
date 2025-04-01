from metodo_numerico import MetodoNumerico

class Euler(MetodoNumerico):
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

    def step(self, t, y, h=None):
        if h is None:
            h = self._h
        dydt = self.system(t, y)
        return [y[i] + h * dydt[i] for i in range(len(y))]

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
