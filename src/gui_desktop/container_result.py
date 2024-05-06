import dearpygui.dearpygui as dpg

# Función para crear y mostrar una nueva ventana
def crear_nueva_ventana(sender, app_data):
    with dpg.window(label="Nueva Ventana"):
        dpg.add_text("Esta es una nueva ventana independiente.")
        dpg.add_button(label="Cerrar", callback=lambda: dpg.delete_item("Nueva Ventana"))

# Crear la interfaz gráfica
with dpg:
    dpg.create_context()

# Crear una nueva ventana fuera del contexto de la ventana principal
# with dpg.window(label="Ventana Principal"):
#     dpg.add_text("Esta es la ventana principal.")
#     dpg.add_button(label="Crear Nueva Ventana", callback=crear_nueva_ventana)

# Crear una nueva ventana independiente
with dpg.window(label="Nueva Ventana", width=300, height=200):
    dpg.add_text("Esta es una nueva ventana independiente.")
    dpg.add_button(label="Cerrar", callback=lambda: dpg.delete_item("Nueva Ventana"))

dpg.create_viewport(title='Ventana Principal', width=500, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
