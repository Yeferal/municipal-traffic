import dearpygui.dearpygui as dpg
from .utils.conf_gui import *
from .node_gui import create_node, create_node_enter, create_node_exit, create_node_rest
from ..objects.graph_node import GraphNode
from ..objects.node_type import NodeType, get_node_type
from ..objects.global_data import get_global_graph
from ..ag.graph_controller import GraphController
from ..objects.model import Model

option_criterion = ["# de Generaciones", "% de Eficiencia"]
option_type_node = [type.name for type in NodeType]
# option_type_node = [type.name for type in NodeType]["CRUCE", "ENTRADA", "SALIDA", "REST"]

def evaluate_model(sender, app_data):
    global_graph = get_global_graph()
    if global_graph is not None:
        name_model = dpg.get_value("input_name_model")
        population = dpg.get_value("input_size_population")
        mutations = dpg.get_value("input_mutations")
        generations = dpg.get_value("input_generations")
        type_criteria = dpg.get_value("combo_criterion")
        criteria = 0
        if type_criteria == "# de Generaciones":
            criteria = dpg.get_value("input_num_generations")
        elif type_criteria == "% de Eficiencia":
            criteria = dpg.get_value("input_efficiency")

        new_model = Model(name_model, population, mutations, generations, type_criteria, criteria, global_graph)
        graph_controller = GraphController()
        graph_controller.init_evaluate(new_model)

    pass

def observer_criterion(sender, app_data):
    if app_data == "# de Generaciones":
        dpg.configure_item("input_num_generations", show=True)
        dpg.configure_item("input_efficiency", show=False)
    elif app_data == "% de Eficiencia":
        dpg.configure_item("input_num_generations", show=False)
        dpg.configure_item("input_efficiency", show=True)


index_nd = 0
def new_node(sender, app_data):
    global_graph = get_global_graph()
    # print(sender, app_data)
    node_name = dpg.get_value("input_id_node")
    type = dpg.get_value("combo_type_node")
    if node_name:
        node_g = GraphNode(node_name, get_node_type(type))
        if global_graph is not None:
            # Crear el nuevo nodo, insetar al grafo y en gui
            if global_graph.insert_node(node_g):
                dpg.set_value("input_id_node", "")
                # crear nodo en el editor
                if type == "ENTER":
                    create_node_enter(node_g.id_node)
                if type == "EXIT":
                    create_node_exit(node_g.id_node)
                if type == "CROSS":
                    create_node(node_g.id_node)
                if type == "REST":
                    create_node_rest(node_g.id_node)

            else:
                # Lanzar error
                pass


def build_left_bar_conf(parent):
    dpg.add_text("Nombre del Modelo", parent=parent)
    dpg.add_input_text(tag="input_name_model", width=(WIDTH_SIDEBAR-20), parent=parent)
    dpg.add_text("Tamanio Poblacion", parent=parent)
    dpg.add_input_int(tag="input_size_population", width=(WIDTH_SIDEBAR-20), parent=parent)
    dpg.add_separator(parent=parent)
    dpg.add_separator(parent=parent)

    with dpg.table(tag="conf_rate", header_row=True, parent=parent):
        dpg.add_table_column(label="X Mutaciones", parent="conf_rate")
        dpg.add_table_column(label="Y generaciones", parent="conf_rate")

        with dpg.table_row(tag="table_rate_rows", parent="conf_rate"):
            dpg.add_input_int(min_value=0, tag="input_mutations", width=(WIDTH_SIDEBAR-20)/2, parent="table_rate_rows")
            dpg.add_input_int(min_value=0, tag="input_generations", width=(WIDTH_SIDEBAR-20)/2, parent="table_rate_rows")

    dpg.add_separator(parent=parent)
    dpg.add_separator(parent=parent)
    dpg.add_text("Criterio de Finalizacion", parent=parent)
    dpg.add_combo(option_criterion, default_value="# de Generaciones", callback=observer_criterion, tag="combo_criterion", parent=parent)
    dpg.add_input_int(min_value=0, step=1, default_value=10, tag="input_num_generations", parent=parent)
    dpg.add_input_float(min_value=0.00, max_value=100, default_value=10.0, tag="input_efficiency", show=False, parent=parent)
    dpg.add_text(parent=parent)
    dpg.add_button(label="Evaluar", callback=evaluate_model, parent=parent)

def build_left_bar_list(parent):
    dpg.add_text("Crear Cruce", parent=parent)
    with dpg.group(tag="container_options_list", label="Opciones de Nodo", horizontal=True, parent=parent):
        dpg.add_input_text(tag="input_id_node", parent="container_options_list", width=((WIDTH_SIDEBAR-20)/2))
        dpg.add_combo(option_type_node, tag="combo_type_node", default_value="ENTER", width=((WIDTH_SIDEBAR-20)/4), parent="container_options_list")
        dpg.add_button(label="Agregar", callback=new_node, parent="container_options_list")
        # dpg.add_button(label="Eliminar", parent="container_options_list")
        # dpg.add_button(label="Editar", parent="container_options_list")

    dpg.add_text("Lista de Carreteras", parent=parent)

    with dpg.table(header_row=True, parent=parent):
        dpg.add_table_column(label="Origen")
        dpg.add_table_column(label="Destino")
        dpg.add_table_column(label="Options")

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_button(label="Press Me 2!")
        dpg.add_button(label="X")