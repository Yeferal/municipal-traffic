from .graph import Graph
from .model import Model

global_graph: Graph = Graph()
global_model: Model = None
global_cancel = True

# Función para establecer el valor de global_var1
def set_global_graph(value):
    global global_graph
    global_graph = value

# Función para obtener el valor de global_var1
def get_global_graph():
    return global_graph

# Función para establecer el valor de global_var2
def set_global_model(value):
    global global_model
    global_model = value

# Función para obtener el valor de global_var2
def get_global_model():
    return global_model

def set_global_cancel(value):
    global global_cancel
    global_cancel = value

# Función para obtener el valor de global_var2
def get_global_cancel():
    return global_cancel