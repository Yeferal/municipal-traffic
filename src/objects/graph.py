from .graph_node import GraphNode
from .edge_street import EdgeStreet


class Graph(object):

    def __init__(self):
        self.nodes = {}

    def insert_node(self, node: GraphNode):
        if node.id_node not in self.nodes:
            self.nodes[node.id_node] = node
            # print(self.nodes[node.id_node])
            return True
        return False

    def insert_edge(self, node_origin, node_destination, capacity, min_percent_time, num_vehicle):
        if node_origin in self.nodes and node_destination in self.nodes:
            # Insetar CALLE
            street = EdgeStreet(node_origin, node_destination, capacity, min_percent_time, num_vehicle)
            self.nodes[node_origin].add_edge(street)

    def delete_node(self, node_origin, node_destination):
        if node_origin in self.nodes and node_destination in self.nodes:
            # self.nodes[node_origin].delete_edge(node_destination)
            pass

    def delete_node_simple(self, id_node):
        if id_node in self.nodes:
            value_deleted = self.nodes.pop(id_node)
            return value_deleted

    def delete_edge(self, node_origin, node_destination):
        if node_origin in self.nodes and node_destination in self.nodes:
            return self.nodes[node_origin].delete_edge(node_destination)

    def get_node(self, id_node):
        return self.nodes[id_node]

    def get_edges(self, id_node):
        if id_node in self.nodes:
            return self.nodes[id_node].edges

    def paint_nodes(self):
        print(self.nodes)
        for node in self.nodes:
            print(node)

    def to_dict(self):
        return {
            "nodes": {str(k): v.to_dict() for k, v in self.nodes.items()}
        }

    @classmethod
    def from_dict(cls, data):
        graph: Graph = cls()
        graph.nodes = {str(k): GraphNode.from_dict(v) for k, v in data["nodes"].items()}
        # print(graph.nodes)
        return graph

    def __str__(self):
        return str(self.nodes)


graph_obj = Graph()
