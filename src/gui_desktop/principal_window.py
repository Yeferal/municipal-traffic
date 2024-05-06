import dearpygui.dearpygui as dpg
from .utils.conf_gui import *
from .menu_bar_gui import build_menu_bar
from .left_bar_edition import build_left_bar_conf, build_left_bar_list
from .node_editor import build_node_editor
from .container_result import build_container_result

# Create the context
dpg.create_context()
# Create the viewport
dpg.create_viewport(title='Traffic', width=WIDTH_INIT, height=HEIGHT_INIT, resizable=True, decorated=True)


# Create the window
with dpg.window(tag="Primary_Window") as primary_window:
    build_menu_bar("Primary_Window")

    with dpg.group(tag="container_tab", horizontal=True, parent=primary_window, pos=(0, HEIGHT_MENU_VAR)) as container_tab:

        with dpg.tab_bar(tag="tab_bar", pos=(200,200), parent=container_tab) as tab_window:
            with dpg.tab(tag="tab_model", label=" MODELO ", parent=tab_window, closable=False):
                # Contenedor de la configuracion del modelo
                with dpg.child_window(tag="container_conf_model",  parent="tab_model") as child_window_conf_model:
                    build_left_bar_conf("container_conf_model")

                # Contenedor de la lista de los grafos o calles
                with dpg.child_window(tag="container_list_street", parent="tab_model") as child_window_list_graph:
                    build_left_bar_list("container_list_street")

                # Contenedor de los grafos, o nodos
                with dpg.child_window(tag="container_editor",pos=(WIDTH_SIDEBAR, 43), parent="tab_model", horizontal_scrollbar=True) as child_window_editor_node:
                    build_node_editor("container_editor")
                pass

            build_container_result("tab_result")


def resize_primary_window():
    x, y = dpg.get_item_rect_size(primary_window)
    # Setter de el contenedor de la configuracion del modelo
    dpg.set_item_height(child_window_conf_model, HEIGHT_WINDOW_CONF_MODEL)
    dpg.set_item_width(child_window_conf_model, WIDTH_SIDEBAR)
    # Setter del contenedor de la lista de grafos
    dpg.set_item_pos(child_window_list_graph, pos=(0, HEIGHT_WINDOW_CONF_MODEL+20))
    dpg.set_item_width(child_window_list_graph, WIDTH_SIDEBAR)
    dpg.set_item_height("container_graphic_plot", (y - 50))
    dpg.set_item_width("container_graphic_plot", (x - 100))
    dpg.set_item_height("container_result_editor", (y - 50))
    dpg.set_item_height("container_result_individuals", (y - 50))
    dpg.set_item_width("container_result_individuals", (x - 100))
    # dpg.set_item_width("container_result_editor", (x - 100))


with dpg.item_handler_registry() as registry:
    dpg.add_item_resize_handler(callback=resize_primary_window)
dpg.bind_item_handler_registry(primary_window, registry)

dpg.setup_dearpygui()
dpg.show_viewport()
# Set the primary window to fullscreen
dpg.set_primary_window("Primary_Window", True)
# Start DearPyGui
dpg.start_dearpygui()
# Destroy the context
dpg.destroy_context()