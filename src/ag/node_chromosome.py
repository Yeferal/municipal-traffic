from ..objects.node_type import NodeType


class NodeChromosome:

    def __init__(self, id_node, edges_street_gene: dict, node_type: NodeType, edges_in: dict, position: tuple):
        self.id_node = id_node
        self.edges_street_gene = edges_street_gene
        self.node_type = node_type
        self.edges_in = edges_in
        self.enters = 0     # Numero de vehiculos ingresados, la suma de los que estan en cola en cada calle que entra
        self.position = position

    def reset_data(self):
        self.enters = 0
        for edge in self.edges_street_gene:
            self.edges_street_gene[edge].reset_data()

    def __str__(self):
        return f"id_node: {self.id_node}, node_type: {self.node_type}, enters: {self.enters}"
