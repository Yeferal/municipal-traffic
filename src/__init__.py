import random

# from .gui_desktop import home
from .gui_desktop import principal_window

# home.save_callback()
def init():
    pass
    # print("Inicio...")
    # home

# init()

import random

class Nodo:
    def __init__(self):
        self.aristas = []

    def agregar_arista(self, valor):
        self.aristas.append(valor)

    def calcular_entrada_nodo(self):
        return sum(self.aristas)

    def repartir_valor_salida(self):
        entrada_total = self.calcular_entrada_nodo()
        valor_salida = round(random.random() * entrada_total)  # Genera un valor aleatorio entre 0 y la entrada total
        valor_salida = 59
        # resta = entrada_total - valor_salida
        resta = valor_salida

        # Verificar si algún valor de arista se hará negativo al restarle la cantidad calculada
        suma_negativos = 0
        for i in range(len(self.aristas)):
            if self.aristas[i] - (resta // len(self.aristas)) < 0:
                print((resta // len(self.aristas)) - self.aristas[i])
                suma_negativos += (resta // len(self.aristas)) - self.aristas[i]
                self.aristas[i] = 0
            else:

                self.aristas[i] -= resta // len(self.aristas)

        suma_negativos += resta - (resta // len(self.aristas))*len(self.aristas)
        # Distribuir el valor restante entre las aristas que no han alcanzado cero
        if suma_negativos != 0:
            for i in range(len(self.aristas)):
                if self.aristas[i] > 0:
                    if self.aristas[i] - (suma_negativos // self.aristas.count(0)) < 0:
                        suma_negativos -= self.aristas[i]
                        self.aristas[i] = 0
                    else:
                        self.aristas[i] -= suma_negativos

        # Actualizar la entrada en el nodo
        entrada_actualizada = entrada_total - valor_salida - suma_negativos
        return valor_salida, entrada_actualizada

# Ejemplo de uso
# nodo = Nodo()
# nodo.agregar_arista(10)
# nodo.agregar_arista(20)
# nodo.agregar_arista(30)
#
# print("Entrada antes de repartir el valor de salida:", nodo.calcular_entrada_nodo())
# valor_salida, entrada_actualizada = nodo.repartir_valor_salida()
# print("Valor de salida:", valor_salida)
# print("Entrada después de repartir el valor de salida:", entrada_actualizada)
# print("Valores de las aristas después de repartir el valor de salida:", nodo.aristas)

