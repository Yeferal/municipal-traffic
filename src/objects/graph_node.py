from .node_type import NodeType
from .edge_street import EdgeStreet


class GraphNode:
    def __init__(self, id_node, node_type: NodeType):
        self.id_node = id_node
        self.node_type = node_type
        self.edges = {}
        self.position = (0, 0)

        # self.edges_in = {}
        # self.weight = 0
        # self.distance = 0
        # self.visited = False
        # self.parent = None
        # self.children = []
        # self.visited = False

    def add_edge(self, edge: EdgeStreet):
        self.edges[(self.id_node, edge.destiny)] = edge

    def delete_edge(self, destiny):
        return self.edges.pop((self.id_node, destiny))

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "node_type": self.node_type,
    #         "edges": self.flatten_dict(),
    #         "position": self.position
    #     }

    def to_dict(self):
        return {
            "id_node": self.id_node,
            "node_type": self.node_type.value,
            "edges": {str(k): v.to_dict() for k, v in self.edges.items()},
            "position": self.position
        }

    @classmethod
    def from_dict(cls, data):
        id_node = data["id_node"]
        node_type = NodeType(data["node_type"])  # Convertir el valor del Enum a Enum
        node: GraphNode = cls(id_node, node_type)
        node.edges = {eval(k): EdgeStreet.from_dict(v) for k, v in data["edges"].items()}  # Convertir las claves de los bordes a enteros
        node.position = data["position"]
        # print(data["edges"])
        # node.__str__()
        return node

    # def flatten_dict(self, prefix=None):
    #     result = {}
    #     for k, v in self.edges():
    #         if prefix:
    #             key = f"{prefix}_{k[0]}_{k[1]}"
    #         else:
    #             key = f"{k[0]}_{k[1]}"
    #         if isinstance(v, dict):
    #             result.update(self.flatten_dict(v, key))
    #         else:
    #             result[key] = v
    #     return result
    def __str__(self):
        # print(f"id: {self.id_node}, node_type: {self.node_type} , edges: {self.edges}")
        return f"id: {self.id_node}, node_type: {self.node_type} , edges: {self.edges}"
