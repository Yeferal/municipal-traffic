import random
import copy
import time

from .graph_individual import GraphIndividual
from .node_chromosome import NodeChromosome
from .edge_street_gene import EdgeStreetGene
from ..objects.node_type import NodeType
from ..objects.global_data import set_global_cancel, get_global_cancel
from ..gui_desktop.container_result import create_plot, build_node_editor_result, build_best_generations, clear_data, set_best_data_individual

class GeneticAlgorithm:

    def __init__(self):
        self.active = True
        self.total_enters = 0

    def run(self, data: dict, population: list):
        self.count_enters(population[0])
        if data['criteria_finished'] == "# de Generaciones":
            generation = 1
            best_from_generation = []
            list_best = []
            list_worst = []
            list_generations = []
            while (data['val_finishes']+1) != generation:
                print(f"Generacion {generation}")
                list_generations.append(generation)
                total_fitness_population = 0
                for individual in population:
                    individual.fitness_value = self.fitness(individual)
                    individual.generation = generation
                    # print(individual)
                    total_fitness_population += individual.fitness_value



                selected_parents = self.selection(population, total_fitness_population)
                new_generation = self.crossover_parents(selected_parents)
                mutation_probability = data['y_generations']/data['x_mutations']
                new_generation = self.mutate(new_generation, mutation_probability)
                population = new_generation
                generation += 1
                for individual in population:
                    individual.fitness_value = self.fitness(individual)

                best_child = max(population, key=lambda x: x.fitness_value)
                worst_child = min(population, key=lambda x: x.fitness_value)

                best_child.efficiency_percentage = best_child.fitness_value/self.total_enters
                worst_child.efficiency_percentage = worst_child.fitness_value / self.total_enters

                list_best.append(best_child.fitness_value)
                list_worst.append(worst_child.fitness_value)
                best_from_generation.append(best_child)
                print(f"Mejor hijo: {best_child}")
                print(f"Peor hijo: {worst_child}")

            clear_data()
            create_plot(list_best, list_worst, list_generations)
            build_node_editor_result(best_child)
            build_best_generations(best_from_generation)
            set_best_data_individual(best_child.fitness_value, best_child.efficiency_percentage)
        else:
            print("Actual state: ", get_global_cancel())
            set_global_cancel(True)
            percentage = 0
            generation = 1
            best_from_generation = []
            list_best = []
            list_worst = []
            list_generations = []
            while (data['val_finishes']/100) > percentage and get_global_cancel():
                print(f"Generacion {generation}")
                list_generations.append(generation)
                total_fitness_population = 0
                for individual in population:
                    individual.fitness_value = self.fitness(individual)
                    individual.generation = generation
                    # print(individual)
                    total_fitness_population += individual.fitness_value

                selected_parents = self.selection(population, total_fitness_population)
                new_generation = self.crossover_parents(selected_parents)
                mutation_probability = data['y_generations'] / data['x_mutations']
                new_generation = self.mutate(new_generation, mutation_probability)
                population = new_generation
                generation += 1
                for individual in population:
                    individual.fitness_value = self.fitness(individual)

                best_child = max(population, key=lambda x: x.fitness_value)
                worst_child = min(population, key=lambda x: x.fitness_value)

                best_child.efficiency_percentage = best_child.fitness_value / self.total_enters
                worst_child.efficiency_percentage = worst_child.fitness_value / self.total_enters
                # print(f"Mejor hijo: {best_child}")
                # print(f"Peor hijo: {worst_child}")
                # Evaluar el porcentage
                if self.total_enters > 0:
                    percentage = best_child.fitness_value/self.total_enters
                print(f"Porcentaje de Eficiencia: {percentage} VS min->{data['val_finishes'] / 100}")
                list_best.append(best_child.fitness_value)
                list_worst.append(worst_child.fitness_value)
                best_from_generation.append(best_child)
                print(f"Mejor hijo: {best_child}")
                print(f"Peor hijo: {worst_child}")

            clear_data()
            create_plot(list_best, list_worst, list_generations)
            build_node_editor_result(best_child)
            build_best_generations(best_from_generation)
            set_best_data_individual(best_child.fitness_value, best_child.efficiency_percentage)

    def mutate(self, new_generation: list, mutation_probability):
        val_random = random.random()
        if val_random <= mutation_probability:
            index_random = random.randint(0, len(new_generation)-1)
            new_generation[index_random] = self.mutate_individual(new_generation[index_random])
        return new_generation

    def mutate_individual(self, individual: GraphIndividual):
        # print(individual.nodes_chromosome)
        random_node_1 = random.choice(list(individual.nodes_chromosome.keys()))
        random_node_2 = random.choice(list(individual.nodes_chromosome.keys()))
        while individual.nodes_chromosome[random_node_1].node_type != NodeType.CROSS:
            random_node_1 = random.choice(list(individual.nodes_chromosome.keys()))

        while individual.nodes_chromosome[random_node_2].node_type != NodeType.CROSS or random_node_1 == random_node_2:
            random_node_2 = random.choice(list(individual.nodes_chromosome.keys()))

        random_gene_1 = random.choice(list(individual.nodes_chromosome[random_node_1].edges_street_gene.keys()))
        random_gene_2 = random.choice(list(individual.nodes_chromosome[random_node_2].edges_street_gene.keys()))

        val_gene_1 = individual.nodes_chromosome[random_node_1].edges_street_gene[random_gene_1].current_percentage
        val_gene_2 = individual.nodes_chromosome[random_node_2].edges_street_gene[random_gene_2].current_percentage
        # #
        individual.nodes_chromosome[random_node_1].edges_street_gene[random_gene_1].current_percentage = val_gene_2
        individual.nodes_chromosome[random_node_2].edges_street_gene[random_gene_2].current_percentage = val_gene_1

        return individual

    def crossover_parents(self, selected_parents: list):
        children = []
        parent_a = None
        parent_b = None
        for i in range(0, len(selected_parents), 2):
            parent_a = selected_parents[i]
            parent_b = selected_parents[i+1]
            # print(f"Cruce de padres: A={parent_a}, B={parent_b}")
            new_children = self.crossover(parent_a, parent_b)
            children.extend(new_children)
        # print(f"HijosNuevo: {children}")
        return children

    def crossover(self, parent_a: GraphIndividual, parent_b: GraphIndividual):
        num_nodes = len(parent_a.nodes_chromosome)
        cross_point = random.randint(1, num_nodes-1)

        partition_a = self.partition_dict(parent_a.nodes_chromosome, cross_point)
        partition_b = self.partition_dict(parent_b.nodes_chromosome, cross_point)
        # print(f"PARTICION =========================================================== Punto de Cruce: {cross_point}")
        # print(f"PadreA: {parent_a.nodes_chromosome}")
        # print(f"PadreB: {parent_b.nodes_chromosome}")
        # print(partition_a[0], partition_a[1])
        # print(partition_b[0], partition_b[1])

        group_a_parente_a = copy.deepcopy(partition_a[0])
        # group_a_parente_a = copy.deepcopy(parent_a.nodes_chromosome[:cross_point])
        group_b_parente_a = copy.deepcopy(partition_a[1])
        # group_b_parente_a = copy.deepcopy(parent_a.nodes_chromosome[cross_point:])
        group_a_parente_b = copy.deepcopy(partition_b[0])
        # group_a_parente_b = copy.deepcopy(parent_b.nodes_chromosome[:cross_point])
        group_b_parente_b = copy.deepcopy(partition_b[1])
        # group_b_parente_b = copy.deepcopy(parent_b.nodes_chromosome[cross_point:])

        children_a = {**group_a_parente_a, **group_b_parente_b}
        children_b = {**group_a_parente_b, **group_b_parente_a}
        # chils_b = group_a_parente_b + group_b_parente_a
        # print("\nHIJOS A: ")
        # print(children_a)
        # print("HIJOS B: ")
        # print(children_b)

        return [GraphIndividual(children_a), GraphIndividual(children_b)]

    @staticmethod
    def partition_dict(dct, split_point):
        """
        Divide un diccionario en partes de tamaño dado.
        """
        part1 = {key: dct[key] for key in list(dct.keys())[:split_point]}
        part2 = {key: dct[key] for key in list(dct.keys())[split_point:]}
        return [part1, part2]

    @staticmethod
    def selection(population: list, total_fitness_population: int):
        print(f"Seleccion por ruleta: total_aptitud => {total_fitness_population}")
        selected_parents = []
        for i in range(len(population)):
            value_random = random.randint(0, total_fitness_population)
            sum_values = 0
            for individual in population:
                sum_values += individual.fitness_value
                if sum_values >= value_random:
                    selected_parents.append(population[i])
                    break
        return selected_parents


    def count_enters(self, individual: GraphIndividual):
        self.total_enters = 0
        for node in individual.nodes_chromosome:
            # Si el nodo es de tipo ENTRADA
            if individual.nodes_chromosome[node].node_type == NodeType.ENTER:
                for edge in individual.nodes_chromosome[node].edges_street_gene:
                    # Usamos los datos de la arista para setear al nodo los datos de la entrada
                    gene: EdgeStreetGene = individual.nodes_chromosome[node].edges_street_gene[edge]
                    self.total_enters += gene.num_vehicle

    def fitness(self, individual: GraphIndividual):
        # SETEA EL NUMERO TOTAL DE CARROS QUE INGRESAN A LOS NODOS INICIALES
        # print(individual)
        for node in individual.nodes_chromosome:
            individual.nodes_chromosome[node].reset_data()
            # Si el nodo es de tipo ENTRADA
            if individual.nodes_chromosome[node].node_type == NodeType.ENTER:
                # recorre las arista para agregar las vehiculos de entrada a cada nodo conectado
                for edge in individual.nodes_chromosome[node].edges_street_gene:
                    # Usamos los datos de la arista para setear al nodo los datos de la entrada
                    gene: EdgeStreetGene = individual.nodes_chromosome[node].edges_street_gene[edge]
                    gene.add_in_line(gene.num_vehicle)
                    individual.nodes_chromosome[gene.destiny].enters = round(gene.num_vehicle*(gene.current_percentage), 0)

        # print(f"\nITERACION 0")
        # for node in individual.nodes_chromosome:
        #     print(individual.nodes_chromosome[node])
        #     for edge in individual.nodes_chromosome[node].edges_street_gene:
        #         gene: EdgeStreetGene = individual.nodes_chromosome[node].edges_street_gene[edge]
        #         print(f"\t{gene}")


        # recorrer los nodos de todo el sitemas, para llenarlo y generara la fluides constante
        for i in range(len(individual.nodes_chromosome)):
            for node in individual.nodes_chromosome:
                # Buscamos un nodo que sea de tipo CRUCE
                if individual.nodes_chromosome[node].node_type == NodeType.CROSS:
                    # RECORREMOS SUS ARISTAS O CALLES
                    total_sender = 0
                    if individual.nodes_chromosome[node].enters > 0:
                        for edge in individual.nodes_chromosome[node].edges_street_gene:
                            # Obetenemos la calle
                            gene: EdgeStreetGene = individual.nodes_chromosome[node].edges_street_gene[edge]
                            if individual.nodes_chromosome[gene.destiny].node_type == NodeType.CROSS:
                                # Si los que estan en cola son menores que el limite entonces pasar los siguientes carros
                                if gene.capacity > gene.in_line:
                                    # NUMERO DE VEHICULOS QUE PODESMO ENVIAR A LA ARISTA TOMANDO LOS INGRESADO Y EL % TIEMPO
                                    num_vehicle_sender = round(individual.nodes_chromosome[node].enters*gene.current_percentage)
                                    # NUMERO DE ESPACIO DISPONIBLE EN LA CARRETERA
                                    in_line_place_available = gene.capacity - gene.in_line
                                    # NUMERO TODAL DE VEHICULOS QUE SE VAN A ENVIAR
                                    if num_vehicle_sender >= in_line_place_available:
                                        num_vehicle_sender = in_line_place_available

                                    # ENVIA LOS VEHICULOS POSIBLES DE ENVIAR
                                    gene.add_in_line(num_vehicle_sender)
                                    total_sender += num_vehicle_sender



                            elif individual.nodes_chromosome[gene.destiny].node_type == NodeType.REST:
                                pass

                            elif individual.nodes_chromosome[gene.destiny].node_type == NodeType.EXIT:
                                num_vehicle_sender = round(individual.nodes_chromosome[node].enters*gene.current_percentage)
                                gene.add_in_line(num_vehicle_sender)
                                total_sender += num_vehicle_sender

                        # ACTUALIZAR LAS CALLES QUE ENTRAN A ESTE NODO
                        self.update_streets_in_line(individual.nodes_chromosome[node], total_sender, individual)

                    individual.nodes_chromosome[node].enters = self.update_enters_in_line(individual.nodes_chromosome[node], individual)



            # print(f"\nITERACION {i+1}")
            # for node in individual.nodes_chromosome:
            #     print(individual.nodes_chromosome[node])
            #     for edge in individual.nodes_chromosome[node].edges_street_gene:
            #         gene: EdgeStreetGene = individual.nodes_chromosome[node].edges_street_gene[edge]
            #         print(f"\t{gene}")
        total_fitness = 0
        for node in individual.nodes_chromosome:
            # Si el nodo es de tipo ENTRADA
            if individual.nodes_chromosome[node].node_type == NodeType.EXIT:
                individual.nodes_chromosome[node].enters += self.update_enters_in_line(individual.nodes_chromosome[node], individual)
                total_fitness += individual.nodes_chromosome[node].enters

        # print(f"\nITERACION SALIDAS")
        # for node in individual.nodes_chromosome:
        #     print(individual.nodes_chromosome[node])
        #     for edge in individual.nodes_chromosome[node].edges_street_gene:
        #         gene: EdgeStreetGene = individual.nodes_chromosome[node].edges_street_gene[edge]
        #         print(f"\t{gene}")
        return total_fitness
    def update_streets_in_line(self, actual_node: NodeChromosome, total_sender, individual: GraphIndividual):
        sum_negative = 0
        new_enters = 0
        for node_in in actual_node.edges_in:
            in_line = individual.nodes_chromosome[node_in].edges_street_gene[(node_in, actual_node.id_node)].in_line
            if in_line - total_sender // len(actual_node.edges_in) < 0:
                sum_negative += (total_sender // len(actual_node.edges_in)) - in_line
                individual.nodes_chromosome[node_in].edges_street_gene[(node_in, actual_node.id_node)].in_line = 0
            else:
                individual.nodes_chromosome[node_in].edges_street_gene[(node_in, actual_node.id_node)].in_line -= (
                        total_sender // len(actual_node.edges_in))
            # print(f"NUEVOS DATOS DESPUES DE LA RESTA DE LOS QUE ESTAN EN COLA: {node_in}: {individual.nodes_chromosome[node_in].edges_street_gene[(node_in, actual_node.id_node)]}")

        # si existe vehiculos restantes por restar en las aristas
        sum_negative += total_sender - (total_sender // len(actual_node.edges_in))*len(actual_node.edges_in)
        if sum_negative != 0:
            new_enters = 0
            for node_in in actual_node.edges_in:
                # print("Entro")
                if individual.nodes_chromosome[node_in].edges_street_gene[(node_in, actual_node.id_node)].in_line > 0:
                    in_line = individual.nodes_chromosome[node_in].edges_street_gene[
                        (node_in, actual_node.id_node)].in_line
                    if (in_line - sum_negative) < 0:
                        sum_negative -= in_line
                        individual.nodes_chromosome[node_in].edges_street_gene[
                            (node_in, actual_node.id_node)].in_line = 0
                    else:
                        individual.nodes_chromosome[node_in].edges_street_gene[
                            (node_in, actual_node.id_node)].in_line -= sum_negative
                    new_enters += individual.nodes_chromosome[node_in].edges_street_gene[
                        (node_in, actual_node.id_node)].in_line


    def update_enters_in_line(self, actual_node: NodeChromosome, individual: GraphIndividual):
        new_enters = 0
        for node_in in actual_node.edges_in:
            in_line = individual.nodes_chromosome[node_in].edges_street_gene[(node_in, actual_node.id_node)].in_line
            new_enters += in_line
        return new_enters