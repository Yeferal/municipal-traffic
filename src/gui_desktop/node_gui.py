import dearpygui.dearpygui as dpg
from ..objects.graph import Graph
from ..objects.graph_node import GraphNode
from ..objects.global_data import get_global_graph

def delete_node(sender, app_data, id_node):
    global_graph = get_global_graph()
    # Primero eliminar de todos los componesntes que entran al nodo
    node_flag: GraphNode = global_graph.get_node(id_node)
    if node_flag:
        if len(node_flag.edges) == 0:
            # con la lista ya podemos buscar los componentes a eliminar
            # Luego si ya se elmminan las calles del cruce salidas, y se elimina el grafo
            if global_graph.delete_node_simple(id_node):
                dpg.delete_item(f"node_{id_node}")
                dpg.delete_item(f"popup_node_{id_node}")

def delete_attr_node(sender, app_data, attr_node):
    global_graph = get_global_graph()
    # print(sender, app_data, attr_node)
    is_active_street = dpg.get_value(sender - 1)
    if is_active_street == "?":
        dpg.delete_item(attr_node)
    else:
        print("No se puede eliminar")

def get_node(sender, app_data, id_node):
    # print(sender, app_data, id_node)
    info = dpg.get_item_info(sender)
    print(info)

def set_node_attribute_capacity(sender, app_data, id_node):
    global_graph = get_global_graph()
    # print(sender, app_data, id_node)
    paret_row = dpg.get_item_parent(sender)
    paret_table = dpg.get_item_parent(paret_row)
    parent_attr = dpg.get_item_parent(paret_table)
    child_title = dpg.get_item_children(parent_attr)
    child_group_title = dpg.get_item_children(child_title[1][0])
    id_text_con = child_group_title[1][1]
    val_con_node = dpg.get_value(id_text_con)
    if val_con_node != "?":
        # print((id_node, val_con_node), app_data)
        # print(global_graph.nodes[id_node].edges)
        global_graph.nodes[id_node].edges[id_node, val_con_node].capacity = app_data
    # dpg.set_value(child_group_title[1][1], "Hola")

def set_node_attribute_num_vehiculos(sender, app_data, id_node):
    global_graph = get_global_graph()
    # print(sender, app_data, id_node)
    child_node = dpg.get_item_children(f"node_{id_node}")
    child_attr = dpg.get_item_children(child_node[1][0])
    child_group_title = dpg.get_item_children(child_attr[1][0])
    value_title = dpg.get_value(child_group_title[1][1])
    if value_title != "?":
        id_input_num_vehicle = child_attr[1][2]
        value_enter = dpg.get_value(id_input_num_vehicle)
        global_graph.nodes[id_node].edges[id_node, value_title].num_vehicle = value_enter

def set_node_attribute_min_time(sender, app_data, id_node):
    global_graph = get_global_graph()
    # print(sender, app_data, id_node)
    paret_row = dpg.get_item_parent(sender)
    paret_table = dpg.get_item_parent(paret_row)
    parent_attr = dpg.get_item_parent(paret_table)
    child_title = dpg.get_item_children(parent_attr)
    child_group_title = dpg.get_item_children(child_title[1][0])
    id_text_con = child_group_title[1][1]
    val_con_node = dpg.get_value(id_text_con)
    if val_con_node != "?":
        # print((id_node, val_con_node), app_data)
        global_graph.nodes[id_node].edges[(id_node, val_con_node)].min_percent_time = round(app_data, 3)
    # print(dpg.get_value(f"street_val_{id_node}"))

def add_attribute_street(sender, app_data, id_node):
    global_graph = get_global_graph()
    with dpg.node_attribute(label="Calle: ", attribute_type=dpg.mvNode_Attr_Output, parent=f"node_{id_node}") as attr_node:
        with dpg.group(horizontal=True, parent=attr_node) as group_title:
            dpg.add_text("Destino:", parent=group_title)
            dpg.add_input_text(default_value="?", enabled=False, width=100, parent=group_title)
            dpg.add_button(label="X", callback=lambda sender, app_data: delete_attr_node(sender, app_data, attr_node), parent=group_title)

        with dpg.table(header_row=True, width=220, parent=attr_node) as tables_attr:
            dpg.add_table_column(label="Capacidad", parent=tables_attr)
            dpg.add_table_column(label="Min % Tiempo", parent=tables_attr)
            with dpg.table_row(parent=tables_attr) as rows_attr:
                dpg.add_input_float(min_value=0.0, min_clamped=True, step=1, width=100, callback=lambda sender, app_data: set_node_attribute_capacity(sender, app_data, id_node), parent=rows_attr)
                dpg.add_input_float(min_value=0.0, max_value=100.0, min_clamped=True, max_clamped=True, width=100, callback=lambda sender, app_data: set_node_attribute_min_time(sender, app_data, id_node), parent=rows_attr)
    # dpg.add_separator(parent=f"node_{id_node}")
        # dpg.set_item_alias()

def build_popup_node(parent, id_node):
    with dpg.popup(parent=parent, mousebutton=dpg.mvMouseButton_Right, tag=f"popup_node_{id_node}"):
        dpg.add_text(f"Opciones Nodo: {id_node}")
        dpg.add_separator()
        dpg.add_button(label="Eliminar", show=True, callback=lambda sender, app_data: delete_node(sender, app_data, id_node))
        # dpg.add_button(label="Eliminar", callback=lambda: dpg.configure_item(f"modal_id_{name_node}", show=False))
        # dpg.add_button(label="Cambiar Nombre", callback=lambda: dpg.configure_item(f"modal_id_{name_node}", show=False))


def create_node(id_node, position=(0,0)):
    with dpg.node(tag=f"node_{id_node}", label=f"Cruce: {id_node}", pos=position, user_data=f"{id_node}", parent="node_editor"):
        build_popup_node(f"node_{id_node}", id_node)
        with dpg.node_attribute(tag=f"input_node_{id_node}", label=f"{id_node}", attribute_type=dpg.mvNode_Attr_Input,
                                shape=dpg.mvNode_PinShape_TriangleFilled, parent=f"node_{id_node}"):
            dpg.add_button(label=" Agregar Calle", width=150, callback=lambda sender, app_data: add_attribute_street(sender, app_data, id_node))


            # print(dpg.get_item_configuration(f"attr_{id_node}"))

def create_node_enter(id_node, position=(0,0)):
    with dpg.node(tag=f"node_{id_node}", label=f"Entrada: {id_node}", pos=position, user_data=f"{id_node}", parent="node_editor"):
        build_popup_node(f"node_{id_node}", id_node)
        with dpg.node_attribute(tag=f"input_node_{id_node}", label=f"{id_node}", attribute_type=dpg.mvNode_Attr_Output,
                                shape=dpg.mvNode_PinShape_TriangleFilled, parent=f"node_{id_node}") as attr_enter:

            with dpg.group(horizontal=True, parent=attr_enter) as group_title:

                dpg.add_text("Destino:", parent=group_title)
                dpg.add_input_text(default_value="?", enabled=False, width=100, parent=group_title)

            dpg.add_text("# Vehiculos:", parent=attr_enter)
            dpg.add_input_int(min_value=0, min_clamped=True, callback=lambda seder, app_data: set_node_attribute_num_vehiculos(seder, app_data, id_node),
                              enabled=True, width=100, parent=attr_enter)
            # dpg.add_button(label=" Agregar Calle", width=150, callback=get_node)


def create_node_exit(id_node, position=(0, 0)):
    with dpg.node(tag=f"node_{id_node}", label=f"Salida: {id_node}", pos=position, user_data=f"{id_node}", parent="node_editor"):
        build_popup_node(f"node_{id_node}", id_node)
        with dpg.node_attribute(tag=f"output_node_{id_node}", label=f"{id_node}", attribute_type=dpg.mvNode_Attr_Input,
                                shape=dpg.mvNode_PinShape_TriangleFilled, parent=f"node_{id_node}"):
            pass
            # dpg.add_button(label=" Agregar Calle", width=150, callback=get_node)


def create_node_rest(id_node, position=(0,0)):
    with dpg.node(tag=f"node_{id_node}", label=f"Rest: {id_node}", pos=position, user_data=f"{id_node}", parent="node_editor"):
        build_popup_node(f"node_{id_node}", id_node)
        with dpg.node_attribute(tag=f"input_node_{id_node}", label=f"{id_node}", attribute_type=dpg.mvNode_Attr_Input,
                                shape=dpg.mvNode_PinShape_TriangleFilled, parent=f"node_{id_node}"):
            pass
            # dpg.add_button(label=" Agregar Calle", width=150, callback=get_node)
