from .graph import Graph
from .graph_node import GraphNode
import pickle


class Model(object):
    def __init__(self, name, population, x_mutations, y_generations, criteria_finished, val_finishes, graph: Graph):
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
        graph = Graph.from_dict(data["graph"])
        return cls(name, population, x_mutations, y_generations, criteria_finished, val_finishes, graph)


model_now = None
