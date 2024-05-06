import dearpygui.dearpygui as dpg
from ..objects.graph import Graph
from ..objects.graph_node import GraphNode
from ..objects.edge_street import EdgeStreet
from ..objects.node_type import NodeType
from ..objects.global_data import get_global_graph

print(get_global_graph())
# def set_instace_graph(graph: Graph):
#     global global_graph
#     global_graph = graph
    # print(global_graph)


def link_callback(sender, app_data):
    global_graph = get_global_graph()
    # print("Link callback called")
    # print(sender, app_data)
    # print(dpg.get_item_parent(app_data[0]))
    # print(dpg.get_item_parent(app_data[1]))
    id_node_origin = dpg.get_item_user_data(dpg.get_item_parent(app_data[0]))
    id_node_destiny = dpg.get_item_user_data(dpg.get_item_parent(app_data[1]))
    # print(id_node_origin, id_node_destiny)
    # print(global_graph)
    node = global_graph.get_node(id_node_origin)
    if node.node_type == NodeType.CROSS:
        capacity = dpg.get_value(app_data[0] + 9)
        min_percet_time = dpg.get_value(app_data[0] + 10)
        global_graph.insert_edge(id_node_origin, id_node_destiny, capacity, min_percet_time, 0)
        # app_data -> (link_id1, link_id2)
        dpg.set_value(app_data[0]+3, id_node_destiny)
    if node.node_type == NodeType.ENTER:
        num_vehicle = dpg.get_value(app_data[0]+5)
        dpg.set_value(app_data[0] + 3, id_node_destiny)
        global_graph.insert_edge(id_node_origin, id_node_destiny, 0, 0, num_vehicle)

    dpg.add_node_link(app_data[0], app_data[1], parent=sender, user_data=app_data)


def link_callback_simple(sender, app_data, edge: EdgeStreet):
    global_graph = get_global_graph()
    # print(sender, app_data)
    id_node_origin = dpg.get_item_user_data(dpg.get_item_parent(app_data[0]))
    id_node_destiny = dpg.get_item_user_data(dpg.get_item_parent(app_data[1]))
    # print(id_node_origin, id_node_destiny)
    # print(global_graph)
    node: GraphNode = global_graph.get_node(id_node_origin)
    if node.node_type == NodeType.CROSS:
        dpg.set_value(app_data[0] + 9, edge.capacity)
        dpg.set_value(app_data[0] + 10, edge.min_percent_time)
        # app_data -> (link_id1, link_id2)
        dpg.set_value(app_data[0]+3, id_node_destiny)
    if node.node_type == NodeType.ENTER:
        dpg.set_value(app_data[0]+5, edge.num_vehicle)
        dpg.set_value(app_data[0] + 3, id_node_destiny)


    dpg.add_node_link(app_data[0], app_data[1], parent=sender, user_data=app_data)

# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    global_graph = get_global_graph()
    # print("Delink callback called")
    # print(sender, app_data)
    id_origin, id_destiny = dpg.get_item_user_data(app_data)
    id_node_origin = dpg.get_item_user_data(dpg.get_item_parent(id_origin))
    id_node_destiny = dpg.get_item_user_data(dpg.get_item_parent(id_destiny))
    global_graph.delete_edge(id_node_origin, id_node_destiny)
    node = global_graph.get_node(id_node_origin)
    if node.node_type == NodeType.CROSS:
        dpg.set_value(id_origin + 3, "?")
    if node.node_type == NodeType.ENTER:
        dpg.set_value(id_origin + 3, "?")
    # app_data -> link_id
    dpg.delete_item(app_data)
    global_graph.paint_nodes()


def get_node(name_node):
    info = dpg.get_item_info(f"{name_node}")
    print(info)


def build_menu_opt_editor():
    with dpg.menu_bar(label="Options"):
        dpg.add_menu_item(label="Nuevo Nodo")


def build_node_editor(parent):
    with dpg.node_editor(tag="node_editor", track_offset=0.5, menubar=False, callback=link_callback,
                         delink_callback=delink_callback, minimap=True,
                         minimap_location=dpg.mvNodeMiniMap_Location_BottomRight, parent=parent) as node_editor:
        pass
