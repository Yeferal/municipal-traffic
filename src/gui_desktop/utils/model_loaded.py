import dearpygui.dearpygui as dpg
from ...objects.graph import Graph, graph_obj
from ...objects.graph_node import GraphNode
from ...objects.model import Model
from ...objects.node_type import NodeType
from ...objects.edge_street import EdgeStreet
from ..node_gui import create_node, create_node_enter, create_node_rest, create_node_exit, add_attribute_street
from ..node_editor import link_callback_simple
# from ..node_editor import link_callback_simple, set_instace_graph
# from ..node_gui import set_instace_graph as set_instances_graph_node_gui
# from ..left_bar_edition import set_instace_graph as set_instances_graph_left_bar_edition


def assemble_components(graph: Graph):
    dpg.delete_item("node_editor", children_only=True)

    # set_instace_graph(graph)
    # set_instances_graph_node_gui(graph)
    # set_instances_graph_left_bar_edition(graph)
    # Agreagar Nodos
    for node in graph.nodes:
        node_f: GraphNode = graph.nodes[node]
        dpg.delete_item(f"popup_node_{node_f.id_node}")
        assemble_nodes(node_f)

    for node in graph.nodes:
        index_child = 1
        for edge in graph.nodes[node].edges:
            edge_f = graph.nodes[node].edges[edge]
            assemble_edges(edge_f, graph.nodes[node].node_type, index_child)
            index_child += 1




def assemble_nodes(node: GraphNode):
    # print(node.__str__())
    if node.node_type == NodeType.ENTER:
        create_node_enter(node.id_node, node.position)
    elif node.node_type == NodeType.CROSS:
        create_node(node.id_node, node.position)
        assemble_street(node.edges)
    elif node.node_type == NodeType.EXIT:
        create_node_exit(node.id_node, node.position)
    elif node.node_type == NodeType.REST:
        create_node_rest(node.id_node, node.position)


def assemble_street(edges):
    for edge in edges:
        # print(edges[edge])
        edge_f: EdgeStreet = edges[edge]
        add_attribute_street(0, None, edge_f.origin)

def assemble_edges(edge: EdgeStreet, node_type: NodeType, index_child):
    parent = "node_editor"
    child_node_origin = dpg.get_item_children(f"node_{edge.origin}")
    child_node_detiny = dpg.get_item_children(f"node_{edge.destiny}")
    # print(f"Origen {edge.origin}:", child_node_origin[1], f", Destino {edge.destiny}:", child_node_detiny[1])

    if node_type == NodeType.ENTER:
        link_callback_simple(parent, (child_node_origin[1][0], child_node_detiny[1][0]), edge)
    elif node_type == NodeType.CROSS:
        link_callback_simple(parent, (child_node_origin[1][index_child], child_node_detiny[1][0]), edge)


def assemble_config(model: Model):
    dpg.set_value("input_name_model", model.name)
    dpg.set_value("input_size_population", model.population)
    dpg.set_value("input_mutations", model.x_mutations)
    dpg.set_value("input_generations", model.y_generations)

    dpg.set_value("combo_criterion", model.criteria_finished)
    if model.criteria_finished == "# de Generaciones":
        dpg.set_value("input_num_generations", model.val_finishes)
    else:
        dpg.set_value("input_efficiency", model.val_finishes)