import dearpygui.dearpygui as dpg

window = dpg.window(tag="Primary Window")

# Create the context
dpg.create_context()

# Create the window
with window:
    # Add content to the window
    dpg.add_text("Hello, world")

# Create the viewport
dpg.create_viewport(title='Home', width=1200, height=700, x_pos=0, y_pos=0, resizable=True, decorated=True)

# Setup DearPyGui
dpg.setup_dearpygui()
dpg.show_viewport()

# Set the primary window to fullscreen
dpg.set_primary_window("Primary Window", True)

# Start DearPyGui
dpg.start_dearpygui()

# Destroy the context
dpg.destroy_context()
