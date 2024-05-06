class Model(object):
    def __init__(self, name, population, x_mutations, y_generations, criteria_finished, val_finishes, graph: GraphNode):
        self.name = name
        self.population = population
        self.x_mutations = x_mutations
        self.y_generations = y_generations
        self.criteria_finished = criteria_finished
        self.val_finishes = val_finishes
        self.graph = graph

    def to_dict(self):
        return {
            "name": self.name,
            "population": self.population,
            "x_mutations": self.x_mutations,
            "y_generations": self.y_generations,
            "criteria_finished": self.criteria_finished,
            "val_finishes": self.val_finishes,
            "graph": self.graph.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        name = data["name"]
        population = data["population"]
        x_mutations = data["x_mutations"]
        y_generations = data["y_generations"]
        criteria_finished = data["criteria_finished"]
        val_finishes = data["val_finishes"]
        graph = GraphNode.from_dict(data["graph"])
        return cls(name, population, x_mutations, y_generations, criteria_finished, val_finishes, graph)
    


class Graph(object):

    def __init__(self):
        self.nodes = {}


    def to_dict(self):
        return {
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()}
        }

    @classmethod
    def from_dict(cls, data):
        graph = cls()
        graph.nodes = {k: GraphNode.from_dict(v) for k, v in data["nodes"].items()}
        print(data["nodes"])
        return graph
    


class GraphNode:
    def __init__(self, id, node_type: NodeType):
        self.id = id
        self.node_type = node_type
        self.edges = {}
        self.position = (0, 0)
    


    def to_dict(self):
        return {
            "id": self.id,
            "node_type": self.node_type.name,
            "edges": {str(k): v.to_dict() for k, v in self.edges.items()},
            "position": self.position
        }

    @classmethod
    def from_dict(cls, data):
        node_type = NodeType(data["node_type"])
        node = cls(data["id"], node_type)
        node.edges = {str(k): EdgeStreet.from_dict(v) for k, v in data["edges"].items()}
        node.position = data["position"]
        return node
    

class EdgeStreet:
    def __init__(self, origin, destiny, capacity, min_percent_time):
        self.origin = origin
        self.destiny = destiny
        self.capacity = capacity
        self.min_percent_time = min_percent_time

    def to_dict(self):
        return {
            "origin": self.origin,
            "destiny": self.destiny,
            "capacity": self.capacity,
            "min_percent_time": self.min_percent_time
        }


    @classmethod
    def from_dict(cls, data):
        return cls(data["origin"], data["destiny"], data["capacity"], data["min_percent_time"])
    

class NodeType(Enum):
    ENTER = 0
    EXIT = 1
    CROSS = 2
    REST = 3