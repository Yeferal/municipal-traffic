import dearpygui.dearpygui as dpg
import pyautogui
from .utils.conf_gui import *
from .node_graph import create_node

# width, height = 1200,800
# width, height = pyautogui.size()
# height_menu_bar = 20

def link_callback(sender, app_data):
    print(sender, app_data)
    # app_data -> (link_id1, link_id2)
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)

# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    print(sender)
    print(app_data)
    # app_data -> link_id
    dpg.delete_item(app_data)

def get_node(name_node):
    info = dpg.delete_item(f"{name_node}")
    print(info)

def build_menu_opt_editor():
    with dpg.menu_bar(label="Options"):
        dpg.add_menu_item(label="Nuevo Nodo")

def build_node_editor():

    with dpg.node_editor(track_offset=0.5, menubar=False, callback=link_callback, delink_callback=delink_callback, minimap=True, minimap_location=dpg.mvNodeMiniMap_Location_BottomRight, tag="node_editor") as node_editor:

        # with dpg.popup("node_editor", mousebutton=dpg.mvMouseButton_Right, tag=f"modal_id"):
        #     pass
        #     dpg.add_text(f"Opciones: ")
        #     dpg.add_button(label="Eliminar",
        #                    callback=lambda: dpg.configure_item(f"modal_id", show=False))
        #     dpg.add_button(label="Cambiar Nombre",
        #                    callback=lambda: dpg.configure_item(f"modal_id", show=False))
        # build_menu_opt_editor()
        # pass
        create_node("Node1")
        create_node("Node2")
        create_node("Node3")
        create_node("Node4")
        create_node("Node5")
        create_node("Node6")






            # with dpg.node(label="Node 1", tag="Node 1"):
            #
            #     with dpg.node_attribute(label="Node A1", attribute_type=dpg.mvNode_Attr_Input, shape=dpg.mvNode_PinShape_TriangleFilled):
            #         dpg.add_button(label=" Agregar Ruta    + ", width=150)
            #         # dpg.add_button(label=" Add Input     + ", width=150)
            #
            #     with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
            #         # dpg.add_table(label="Node")
            #         # dpg.add_text("Nombre Salida")
            #         with dpg.table(header_row=False, width=300):
            #
            #             # use add_table_column to add columns to the table,
            #             # table columns use child slot 0
            #             dpg.add_table_column()
            #             dpg.add_table_column()
            #             with dpg.table_row():
            #                 dpg.add_text("Nombre Salida")
            #                 dpg.add_button(label="Quitar")
            #                 # dpg.add_text("---")
            #
            #         # dpg.add_button(label="Nombre Salida")
            #         dpg.add_input_float(label="Capacidad", width=150)
            #         dpg.add_input_float(label="% Tiempo-Paso", width=150)
            #         dpg.add_input_float(label="RED", width=150)
            #         # dpg.add_text("sdfs")
