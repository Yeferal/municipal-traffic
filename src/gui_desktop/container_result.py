import dearpygui.dearpygui as dpg
from ..objects.global_data import set_global_cancel
from ..ag.graph_individual import GraphIndividual
from ..ag.node_chromosome import NodeChromosome
from ..ag.edge_street_gene import EdgeStreetGene
from ..objects.node_type import NodeType

def stop_iteration(sender, app_data):
    print("CANCELLED")
    set_global_cancel(False)
def link_callback_simple(sender, app_data, edge: EdgeStreetGene, individual: GraphIndividual):
    # print(sender, app_data)
    id_node_origin = dpg.get_item_user_data(dpg.get_item_parent(app_data[0]))
    id_node_destiny = dpg.get_item_user_data(dpg.get_item_parent(app_data[1]))
    # print(id_node_origin, id_node_destiny)
    # print(global_graph)
    node: NodeChromosome = individual.nodes_chromosome[id_node_origin]
    if node.node_type == NodeType.CROSS:
        dpg.set_value(app_data[0] + 8, edge.capacity)
        dpg.set_value(app_data[0] + 9, (edge.current_percentage*100))
        # app_data -> (link_id1, link_id2)
        dpg.set_value(app_data[0]+3, id_node_destiny)
    if node.node_type == NodeType.ENTER:
        dpg.set_value(app_data[0]+5, edge.num_vehicle)
        dpg.set_value(app_data[0] + 3, id_node_destiny)


    dpg.add_node_link(app_data[0], app_data[1], parent=sender, user_data=app_data)

def clear_data():
    dpg.delete_item("container_graphic_plot", children_only=True)
    dpg.delete_item("node_editor_result", children_only=True)
    dpg.delete_item("container_result_individuals", children_only=True)
def build_node_editor_result(best_individual: GraphIndividual):
    dpg.delete_item("node_editor_result", children_only=True)
    for node in best_individual.nodes_chromosome:
        node_f: NodeChromosome = best_individual.nodes_chromosome[node]
        assemble_nodes(node_f)

    for node in best_individual.nodes_chromosome:
        index_child = 1
        for edge in best_individual.nodes_chromosome[node].edges_street_gene:
            edge_f = best_individual.nodes_chromosome[node].edges_street_gene[edge]
            assemble_edges(edge_f, best_individual.nodes_chromosome[node].node_type, index_child, best_individual)
            index_child += 1


def assemble_nodes(node: NodeChromosome):
    # print(node.__str__())
    if node.node_type == NodeType.ENTER:
        create_node_enter(node.id_node, node.position)
    elif node.node_type == NodeType.CROSS:
        create_node_cross(node.id_node, node.position)
        assemble_street(node.edges_street_gene)
    elif node.node_type == NodeType.EXIT:
        create_node_exit(node.id_node, node.position)
    elif node.node_type == NodeType.REST:
        create_node_rest(node.id_node, node.position)

def assemble_street(edges):
    for edge in edges:
        edge_f: EdgeStreetGene = edges[edge]
        add_attribute_street(0, None, edge_f.origin)

def assemble_edges(edge: EdgeStreetGene, node_type: NodeType, index_child, individual: GraphIndividual):
    parent = "node_editor_result"
    child_node_origin = dpg.get_item_children(f"nodeR_{edge.origin}")
    child_node_detiny = dpg.get_item_children(f"nodeR_{edge.destiny}")
    # print(f"Origen {edge.origin}:", child_node_origin[1], f", Destino {edge.destiny}:", child_node_detiny[1])

    if node_type == NodeType.ENTER:
        link_callback_simple(parent, (child_node_origin[1][0], child_node_detiny[1][0]), edge, individual)
    elif node_type == NodeType.CROSS:
        link_callback_simple(parent, (child_node_origin[1][index_child], child_node_detiny[1][0]), edge, individual)


def add_attribute_street(sender, app_data, id_node):
    with dpg.node_attribute(label="Calle: ", attribute_type=dpg.mvNode_Attr_Output, parent=f"nodeR_{id_node}") as attr_node:
        with dpg.group(horizontal=True, parent=attr_node) as group_title:
            dpg.add_text("Destino:", parent=group_title)
            dpg.add_input_text(default_value="?", enabled=False, width=100, parent=group_title)

        with dpg.table(header_row=True, width=220, parent=attr_node) as tables_attr:
            dpg.add_table_column(label="Capacidad", enabled=False, parent=tables_attr)
            dpg.add_table_column(label="% Tiempo", enabled=False, parent=tables_attr)
            with dpg.table_row(parent=tables_attr) as rows_attr:
                dpg.add_input_float(enabled=False, min_value=0.0, min_clamped=True, step=1, width=100, parent=rows_attr)
                dpg.add_input_float(enabled=False, min_value=0.0, max_value=100.0, min_clamped=True, max_clamped=True, width=100, parent=rows_attr)

def set_best_data_individual(num_vehicle, percent_efficiency):
    dpg.set_value("best_num_veh_result", num_vehicle)
    dpg.set_value("best_percent_veh_result", percent_efficiency)


def create_node_cross(id_node, position=(0,0)):
    with dpg.node(tag=f"nodeR_{id_node}", label=f"Cruce: {id_node}", pos=position, user_data=f"{id_node}", parent="node_editor_result"):
        with dpg.node_attribute(tag=f"input_nodeR_{id_node}", label=f"{id_node}", attribute_type=dpg.mvNode_Attr_Input,
                                shape=dpg.mvNode_PinShape_TriangleFilled, parent=f"nodeR_{id_node}"):
            pass

def create_node_enter(id_node, position=(0,0)):
    with dpg.node(tag=f"nodeR_{id_node}", label=f"Entrada: {id_node}", pos=position, user_data=f"{id_node}", parent="node_editor_result"):
        with dpg.node_attribute(tag=f"input_nodeR_{id_node}", label=f"{id_node}", attribute_type=dpg.mvNode_Attr_Output,
                                shape=dpg.mvNode_PinShape_TriangleFilled, parent=f"nodeR_{id_node}") as attr_enter:

            with dpg.group(horizontal=True, parent=attr_enter) as group_title:

                dpg.add_text("Destino:", parent=group_title)
                dpg.add_input_text(default_value="?", enabled=False, width=100, parent=group_title)

            dpg.add_text("# Vehiculos:", parent=attr_enter)
            dpg.add_input_int(min_value=0, min_clamped=True, enabled=False, width=100, parent=attr_enter)


def create_node_exit(id_node, position=(0, 0)):
    with dpg.node(tag=f"nodeR_{id_node}", label=f"Salida: {id_node}", pos=position, user_data=f"{id_node}", parent="node_editor_result"):
        with dpg.node_attribute(tag=f"output_nodeR_{id_node}", label=f"{id_node}", attribute_type=dpg.mvNode_Attr_Input,
                                shape=dpg.mvNode_PinShape_TriangleFilled, parent=f"nodeR_{id_node}"):
            pass


def create_node_rest(id_node, position=(0,0)):
    with dpg.node(tag=f"nodeF_{id_node}", label=f"Rest: {id_node}", pos=position, user_data=f"{id_node}", parent="node_editor_result"):
        with dpg.node_attribute(tag=f"input_nodeR_{id_node}", label=f"{id_node}", attribute_type=dpg.mvNode_Attr_Input,
                                shape=dpg.mvNode_PinShape_TriangleFilled, parent=f"nodeR_{id_node}"):
            pass

def build_container_result(parent):
    with dpg.tab(tag="tab_result", label="Resultado", closable=False, parent=parent) as tab_result:
        dpg.add_text("\tDATOS DEL MEJOR INDIVIDUO DE LA ULTIMA GENERACION")
        with dpg.group(tag="bets_resulta_individual", horizontal=True, parent=tab_result):
            dpg.add_text("\t# VEHICULOS QUE SALES:")
            dpg.add_text("", tag="best_num_veh_result")
            dpg.add_text("\t% Eficiencia:")
            dpg.add_text("", tag="best_percent_veh_result")

        with dpg.group(tag="container_option", horizontal=True, parent=tab_result):
            dpg.add_button(label=" LIMPIAR ", callback=clear_data)
            dpg.add_button(label=" CANCELAR RECORRIDO ", callback=stop_iteration)
        dpg.add_separator()

        with dpg.group(tag="container_graphic_plot", parent=tab_result):
            pass

        with dpg.group(tag="container_result_individuals", parent=tab_result):
            build_best_generations([])

        with dpg.group(tag="container_result_editor", parent=tab_result, tracked=True) as container_draw:
            with dpg.node_editor(tag="node_editor_result", track_offset=0.5, menubar=False, minimap=True, height=700,
                                 minimap_location=dpg.mvNodeMiniMap_Location_BottomRight, parent=container_draw) as container_editor_graph:
                pass




def create_plot(list_best, list_worst, list_generations):
    dpg.delete_item("container_graphic_plot", children_only=True)
    with dpg.plot(tag="plot_line", label="Line Series", parent="container_graphic_plot"):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Generation")
        dpg.add_plot_axis(dpg.mvYAxis, label="Fitness", tag="y_axis")

        # series belong to a y axis
        dpg.add_line_series(list_generations, list_best, label="MEJORES", parent="y_axis")
        dpg.add_line_series(list_generations, list_worst, label="PEORES", parent="y_axis")

def build_best_generations(list_best: list):
    dpg.delete_item("container_result_individuals", children_only=True)
    with dpg.table(tag="table_result", header_row=True, scrollX=True, parent="container_result_individuals") as tables_res:
        dpg.add_table_column(label=" # Generacion ", enabled=False, parent="table_result")
        dpg.add_table_column(label=" % Eficiencia ", enabled=False, parent="table_result")
        dpg.add_table_column(label=" Cantidad Vehiculos Salen ", enabled=False, parent="table_result")
        for i in range(len(list_best)):
            individual: GraphIndividual = list_best[i]
            with dpg.table_row(parent="table_result") as rows_result:
                dpg.add_text(f" {i+1} ")
                dpg.add_text(f" {individual.efficiency_percentage} ")
                dpg.add_text(f" {individual.fitness_value} ")
