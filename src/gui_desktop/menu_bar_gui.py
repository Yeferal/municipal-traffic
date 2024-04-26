import dearpygui.dearpygui as dpg
from .utils.conf_gui import *
def print_me(sender):
    print(f"Menu Item: {sender}")

def close_program(sender):
    dpg.stop_dearpygui()

def build_menu_bar():
    with dpg.viewport_menu_bar():
        with dpg.menu(label="Modelo"):
            dpg.add_menu_item(label="Crear Modelo", callback=print_me, tag="create_model")
            dpg.add_menu_item(label="Cargar Modelo", callback=print_me, tag="load_model")
            dpg.add_menu_item(label="Guardar Como", callback=print_me, tag="save_as", enabled=False)
            dpg.add_menu_item(label="Guardar Modelo", callback=print_me, tag="save", shortcut="Ctrl + S", enabled=False)

        # with dpg.menu(label="Evaluar Modelo"):
        #     dpg.add_menu_item(label="Evaluar", callback=print_me, tag="eval_model")

        dpg.add_menu_item(label="Cerrar Programa", callback=close_program)

        #     with dpg.menu(label="Settings"):
        #         dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
        #         dpg.add_menu_item(label="Setting 2", callback=print_me)
        #
        # dpg.add_menu_item(label="Help", callback=print_me)
        #
        # with dpg.menu(label="Widget Items"):
        #     dpg.add_checkbox(label="Pick Me", callback=print_me)
        #     dpg.add_button(label="Press Me", callback=print_me)
        #     dpg.add_color_picker(label="Color Me", callback=print_me)

    # dpg.add_button(label="Salir", callback=print_me)