import random
import threading

from ..objects.graph import Graph
from ..objects.model import Model
from ..objects.graph_node import GraphNode
from ..objects.edge_street import EdgeStreet
from .edge_street_gene import EdgeStreetGene
from .node_chromosome import NodeChromosome
from .graph_individual import GraphIndividual
from .genetic_algorithm import GeneticAlgorithm
from ..objects.global_data import set_global_cancel, get_global_cancel

import copy

from ..objects.node_type import NodeType


class GraphController:

    def init_evaluate(self, model: Model):
        # Generar el individuo base
        individual_base = self.transform_graph(model.graph)
        # Generar la poblacion
        population = []
        for i in range(model.population):
            individual_copy = copy.deepcopy(individual_base)
            for node in individual_copy.nodes_chromosome:
                # generar los % de tiempo para las calles del individuo
                self.generate_percentage_street(individual_copy.nodes_chromosome[node])
            population.append(individual_copy)
            # break
        # print(population)
        # ENVIAR AL AG
        ag = GeneticAlgorithm()
        data_model = {'population': model.population, 'x_mutations': model.x_mutations,
                      'y_generations': model.y_generations, 'criteria_finished': model.criteria_finished,
                      'val_finishes': model.val_finishes}

        set_global_cancel(True)
        # Crear un hilo para ejecutar la función
        thread = threading.Thread(target=ag.run(data_model, population))
        # Iniciar el hilo
        thread.start()
        # thread.join()


    def transform_graph(self, graph):
        list_node = graph.nodes
        list_edge_in_node = {}
        list_chromosome_node = {}
        for node in list_node:
            list_edge_in_node[node] = []

        for node in list_node:
            list_edge_gene = {}
            for edge in graph.nodes[node].edges:
                gene = self.transform_edge(graph.nodes[node].edges[edge])
                # agrega los nodos que tiene conexion con el nodo de destino, las calles que ingresan con el nodo de
                # destino
                list_edge_in_node[gene.destiny].append(gene.origin)
                # Agrega el gen arista a al dicionario
                list_edge_gene[edge] = gene
            # crea y agrega el nuevo cromosoma nodo
            node_chromosome = self.transform_node(graph.nodes[node], list_edge_gene)
            list_chromosome_node[node] = node_chromosome

        for node in list_edge_in_node:
            list_chromosome_node[node].edges_in = list_edge_in_node[node]

        # Generamos el individuo para luego clonarlo
        graph_individual = GraphIndividual(list_chromosome_node)
        return graph_individual

    @staticmethod
    def transform_node(node: GraphNode, edges_gene: dict):
        return NodeChromosome(node.id_node, edges_gene, node.node_type, {}, node.position)

    @staticmethod
    def transform_edge(edge: EdgeStreet):
        return EdgeStreetGene(edge.origin, edge.destiny, edge.capacity, edge.min_percent_time, edge.num_vehicle)

    @staticmethod
    def generate_percentage_individual(individual: GraphIndividual):
        pass

    @staticmethod
    def generate_percentage_street(node: NodeChromosome):
        # print(node.id_node)
        size_edges = len(node.edges_street_gene)
        percentage_total = 100
        minimum_percentages = []

        if node.node_type == NodeType.ENTER:
            percentages = [round((percentage_total / size_edges), 3) for _ in range(size_edges)]
            # print(percentages)
        if node.node_type == NodeType.EXIT:
            # percentages = [round((percentage_total/size_edges), 3) for _ in range(size_edges)]
            # print(percentages)
            pass
        if node.node_type == NodeType.REST:
            percentages = [round((percentage_total / size_edges), 3) for _ in range(size_edges)]
            # print(percentages)

        if node.node_type == NodeType.CROSS:
            for edge in node.edges_street_gene:
                minimum_percentages.append(node.edges_street_gene[edge].min_percent_time)

            # Verificar que la suma de los porcentajes mínimos sea menor o igual al total
            if sum(minimum_percentages) > percentage_total:
                raise ValueError("La suma de los porcentajes mínimos supera el total")
            percentages = []
            if size_edges == 1:
                percentages = [100.0]
            else:
                # Generar N números aleatorios que sumen total_porcentaje - suma de los porcentajes mínimos
                percentages = [round(random.uniform(0, percentage_total - sum(minimum_percentages)), 3) for _ in
                               range(size_edges)]
            # print(f"Primero-> {percentages} VS {minimum_percentages}")
            # Ajustar los porcentajes aleatorios para cumplir con los porcentajes mínimos
            for i in range(size_edges):
                min_percentage = minimum_percentages[i]
                if min_percentage > percentages[i]:
                    # Si el porcentaje aleatorio es menor que el mínimo, lo ajustamos al mínimo
                    percentages[i] = round(min_percentage, 3)
                    # print(f"Entro1-> {percentages}")
                elif min_percentage <= percentages[i]:
                    # Si el porcentaje aleatorio es mayor que el mínimo, reducimos los otros porcentajes
                    dif = percentages[i] - min_percentage
                    for j in range(size_edges):
                        if j != i and percentages[j] - dif >= minimum_percentages[j]:
                            percentages[j] -= dif
                            percentages[j] = round(percentages[j], 3)
                            break
                    # print(f"Salio2-> {percentages}")
            # print(percentages)

        keys_edges = list(node.edges_street_gene.keys())
        for i in range(len(keys_edges)):
            node.edges_street_gene[keys_edges[i]].current_percentage = percentages[i]/100
            # print(node.edges_street_gene[keys_edges[i]])

        return node

    @staticmethod
    def generate_percentage_traffic_light(min_percetage, max_percetage):
        return random.uniform(min_percetage, max_percetage)
