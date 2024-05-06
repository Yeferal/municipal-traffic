from src.objects.node_type import NodeType


class GraphIndividual(object):
    def __init__(self, nodes_chromosome: dict):
        self.nodes_chromosome = nodes_chromosome
        self.fitness_value = 0
        self.generation = 1
        self.nodes_cross = 0
        self.efficiency_percentage = 0.00


    def generate_nodes_not_enter_or_exit(self):
        num_nodes = 0
        pos_nodes = []
        # for node in self.nodes_chromosome:
        #     if self.nodes_chromosome[node].node_type != NodeType.CROSS:
        #         num_nodes += 1
        #         pos_nodes.append(node)
        # self.nodes_cross = num_nodes
        return num_nodes, pos_nodes
    def __str__(self):
        # return str(f"nodes: {self.nodes_chromosome}, fitness_value: {self.fitness_value}")
        return str(f"nodes: {len(self.nodes_chromosome)}, fitness_value: {self.fitness_value}")
