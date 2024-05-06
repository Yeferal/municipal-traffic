import dearpygui.dearpygui as dpg
from .utils.conf_gui import *
from ..objects.model import Model, model_now
from ..objects.utils.file_control import save_json, load_json
from ..objects.graph import Graph
from .utils.model_loaded import assemble_components, assemble_config
from ..objects.global_data import set_global_model, set_global_graph, get_global_graph, get_global_model

# def set_instace_graph(graph: Graph):
#     global global_graph
#     global_graph = graph
#     print(global_graph)
def save_as_model(sender, app_data):
    global_graph = get_global_graph()
    global_model = get_global_model()
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

    # Update coordinates
    for node in global_graph.nodes:
        pos = dpg.get_item_pos(f"node_{node}")
        global_graph.nodes[node].position = pos

    # print(name_model, population, mutations, generations, type_criteria, criteria, global_graph)
    new_model = Model(name_model, population, mutations, generations, type_criteria, criteria, global_graph)
    # model = Model(name_model, population, mutations, generations, type_criteria, criteria, global_graph)
    set_global_model(new_model)
    model_dict = new_model.to_dict()
    save_json(name_model, model_dict)


def save_model(sender, app_data):
    global_graph = get_global_graph()
    if global_graph is None:
        save_as_model(sender, app_data)
    else:
        #     Captura todas los datos
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
        # print(name_model, population, mutations, generations, type_criteria, criteria, None)
        new_model = Model(name_model, population, mutations, generations, type_criteria, criteria, global_graph)
        set_global_model(new_model)
        model_dict = new_model.to_dict()
        save_json(name_model, model_dict)



# Función que se llama cuando se selecciona un archivo
def on_file_selected(sender, app_data, user_data):
    global_graph = get_global_graph()
    global_model = get_global_model()
    print("Sender: ", sender)
    print("App Data: ", app_data)
    file_path = app_data["file_path_name"]
    print("Ruta del archivo seleccionado:", file_path)

    model = load_json(file_path)
    # model = load_json("C:\\Users\\Usuario\\Documents\\PycharmProjects\\MunicipalTraffic\\models\\Modelo1.json")

    global_model = model
    global_graph = global_model.graph
    set_global_model(model)
    set_global_graph(model.graph)
    # print(global_graph)
    assemble_components(global_graph)
    assemble_config(global_model)


def close_program(sender):
    dpg.stop_dearpygui()

def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)

def build_menu_bar(parent):
    with dpg.viewport_menu_bar(parent=parent):
        with dpg.menu(label="Modelo"):
            # dpg.add_menu_item(label="Crear Modelo", tag="create_model")
            dpg.add_menu_item(label="Cargar Modelo",
                              callback=lambda: dpg.show_item("file_dialog_tag"), tag="load_model")
            # dpg.add_menu_item(label="Cargar Modelo",
            #                   callback=on_file_selected, tag="load_model")
            dpg.add_menu_item(label="Guardar Como", callback=save_as_model, tag="save_as")
            dpg.add_menu_item(label="Guardar Modelo", callback=save_model, tag="save", shortcut="Ctrl + S")

        dpg.add_menu_item(label="Cerrar Programa", callback=close_program)


    with dpg.file_dialog(directory_selector=False, show=False, callback=on_file_selected, id="file_dialog_tag", width=700,
                         height=400, default_path="./models"):
        dpg.add_file_extension(".json")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp, .pkl}", color=(0, 255, 255, 255))
        dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")
        # dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]")
        dpg.add_file_extension(".json", color=(0, 255, 0, 255), custom_text="[JSON]")
