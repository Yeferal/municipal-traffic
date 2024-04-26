import dearpygui.dearpygui as dpg

def get_node(name_node):
    dpg.get_item_info(f"{name_node}")

def delete_node(sender, app_data):
    print(sender)
    print(dpg.get_item_parent(sender))
    print(dpg.get_item_parent(dpg.get_item_parent(sender)))
    dpg.delete_item("Node1")

def create_node(name_node):
    with dpg.node(label=f"{name_node}", tag=f"{name_node}") as node:
        with dpg.popup(node, mousebutton=dpg.mvMouseButton_Right, tag=f"modal_id_{name_node}"):
            dpg.add_text(f"Opciones: {name_node}\n")
            dpg.add_button(label="Eliminar", callback=delete_node, show=True)
            # dpg.add_button(label="Eliminar", callback=lambda: dpg.configure_item(f"modal_id_{name_node}", show=False))
            dpg.add_button(label="Cambiar Nombre", callback=lambda: dpg.configure_item(f"modal_id_{name_node}", show=False))

        with dpg.node_attribute(label=f"{name_node}", attribute_type=dpg.mvNode_Attr_Input, shape=dpg.mvNode_PinShape_TriangleFilled):
            dpg.add_button(label=" Agregar Ruta    + ", width=150, callback=get_node(f"{name_node}"))
            # dpg.add_button(label=" Add Input     + ", width=150)

        with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
            # dpg.add_table(label="Node")
            # dpg.add_text("Nombre Salida")
            with dpg.table(header_row=False, width=300):
                # use add_table_column to add columns to the table,
                # table columns use child slot 0
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text("Nombre Salida")
                    dpg.add_button(label="Quitar")
                    # dpg.add_text("---")

            # dpg.add_button(label="Nombre Salida")
            dpg.add_input_float(label="Capacidad", width=150)
            dpg.add_input_float(label="% Tiempo-Paso", width=150)
            dpg.add_input_float(label="RED", width=150)
            # dpg.add_text("sdfs")

