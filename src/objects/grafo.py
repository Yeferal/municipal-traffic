class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, vertice):
        if vertice not in self.vertices:
            self.vertices[vertice] = []

    def agregar_arista(self, origen, destino):
        if origen in self.vertices and destino in self.vertices:
            self.vertices[origen].append(destino)
            self.vertices[destino].append(origen)  # Agregar esta línea si el grafo es no dirigido

    def obtener_vertices(self):
        return list(self.vertices.keys())

    def obtener_aristas(self):
        aristas = []
        for vertice, vecinos in self.vertices.items():
            for vecino in vecinos:
                if (vecino, vertice) not in aristas:
                    aristas.append((vertice, vecino))
        return aristas

    def __str__(self):
        return f"Vertices: {self.obtener_vertices()}, Aristas: {self.obtener_aristas()}"

# Ejemplo de uso
grafo = Grafo()
grafo.agregar_vertice('A')
grafo.agregar_vertice('B')
grafo.agregar_vertice('C')
grafo.agregar_arista('A', 'B')
grafo.agregar_arista('B', 'C')
print(grafo)
