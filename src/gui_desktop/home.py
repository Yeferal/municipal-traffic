import dearpygui.dearpygui as dpg

from .utils.conf_gui import *
from .menu_bar_gui import build_menu_bar

from .left_bar_edition import build_left_bar_conf, build_left_bar_list
from .node_editor import build_node_editor

def print_me(sender):
    print(f"Menu Item: {sender}")

# callback runs when user attempts to connect attributes


def change_text(sender, app_data):
    print("hola", sender)
    # dpg.set_value("text_item", f"Mouse Button: {app_data[0]}, Down Time: {app_data[1]} seconds")

def get_width_height():
    info = dpg.get_item_rect_size("Primary Window")
    print(info)

# Create the context
dpg.create_context()
# Create the viewport
dpg.create_viewport(title='Home', width=1000, height=600, x_pos=0, y_pos=0, resizable=True, decorated=True)

# Create the window
with dpg.window(tag="Primary Window") as primary_window:

    build_menu_bar()

    with dpg.child_window(pos=(0,HEIGHT_MENU_VAR)) as child_window_conf_model:
        build_left_bar_conf()

    with dpg.child_window() as child_window_list_graph:
        build_left_bar_list()

    with dpg.child_window(pos=(WIDTH_SIDEBAR, HEIGHT_MENU_VAR)) as child_window_editor_node:
        # pass
        # with dpg.add_window("sdf",tag="test", parent=child_window_editor_node):
        #     pass
        # with dpg.popup(modal=False, parent="test"):
        #     dpg.add_text("This is a popup")
        # dpg.add_button(label="Close", callback=lambda: dpg.configure_item("contain_editor", show=False))
        build_node_editor()

    # print(dpg.get_value("combo_criterion"))
def resize_primary_window():
    x, y = dpg.get_item_rect_size(primary_window)
    # print(x, y)
    # dpg.set_item_height(child_window, ((y * 0.5)))
    dpg.set_item_height(child_window_conf_model, HEIGHT_WIDOW_CONF_MODEL)
    dpg.set_item_width(child_window_conf_model, WIDTH_SIDEBAR)
    # dpg.set_item_width(child_window, x * 0.5)

    # dpg.set_item_pos(child_window_list_graph,pos=(0,((y * 0.5)+20)))
    dpg.set_item_pos(child_window_list_graph, pos=(0, HEIGHT_WIDOW_CONF_MODEL+20))
    # dpg.set_item_height(child_window_list_graph, ((y * 0.5)-10))
    dpg.set_item_width(child_window_list_graph, WIDTH_SIDEBAR)
    # dpg.set_item_width(child_window_list_graph, x * 0.5)


with dpg.item_handler_registry() as registry:
    dpg.add_item_resize_handler(callback=resize_primary_window)
dpg.bind_item_handler_registry(primary_window, registry)

# Setup DearPyGui
dpg.setup_dearpygui()
dpg.show_viewport()
# Set the primary window to fullscreen
dpg.set_primary_window("Primary Window", True)
# Start DearPyGui
dpg.start_dearpygui()
# Destroy the context
dpg.destroy_context()
