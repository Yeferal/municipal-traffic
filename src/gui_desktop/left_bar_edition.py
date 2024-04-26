import dearpygui.dearpygui as dpg
from .utils.conf_gui import *

option_criterion = ["# de Generaciones", "% de Eficiencia"]
def observer_criterion(sender, app_data):
    # print(sender)
    # print(app_data)
    if app_data == "# de Generaciones":
        dpg.configure_item("input_num_generations", show=True)
        dpg.configure_item("input_efficiency", show=False)
    elif app_data == "% de Eficiencia":
        dpg.configure_item("input_num_generations", show=False)
        dpg.configure_item("input_efficiency", show=True)
def build_left_bar_conf():
    dpg.add_text("Nombre del Modelo")
    dpg.add_input_text(tag="input_name_model")
    dpg.add_text("Tamanio Poblacion")
    dpg.add_input_int(tag="input_size_population")
    dpg.add_separator()
    dpg.add_separator()
    with dpg.table(header_row=True):
        dpg.add_table_column(label="X Mutaciones")
        dpg.add_table_column(label="Y generaciones")
        with dpg.table_row():
            dpg.add_input_int(min_value=0, tag="input_mutantions")
            dpg.add_input_int(min_value=0, tag="input_generations")
    dpg.add_separator()
    dpg.add_separator()
    dpg.add_text("Criterio de Finalizacion")
    dpg.add_combo(option_criterion, default_value="# de Generaciones", callback=observer_criterion, tag="combo_criterion")
    dpg.add_input_int(min_value=0, step=1, default_value=10, tag="input_num_generations")
    dpg.add_input_float(min_value=0.00, max_value=100, default_value=10.0, tag="input_efficiency", show=False)
    dpg.add_text()
    dpg.add_button(label="Evaluar")

def build_left_bar_list():
    dpg.add_text("Lista de Carreteras")
    with dpg.table(header_row=True):
        dpg.add_table_column(label="Origen")
        dpg.add_table_column(label="Destino")
        dpg.add_table_column(label="Options")

    with dpg.group(horizontal=True):
        dpg.add_button(label="Press Me 2!")
        dpg.add_button(label="X")