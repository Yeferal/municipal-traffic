import pickle
import json
from ..model import Model


def save_json(filename, data):
    try:
        with open(f"./models/{filename}.json", "w") as f:
            json.dump(data, f)
        print(f"Objeto guardado correctamente en el archivo '{filename}'")
    except Exception as e:
        print("Ocurrió un error al guardar el archivo:", e)



def load_json(filename):
    with open(f"{filename}", "r") as f:
        model_dict = json.load(f)
        # for i in model_dict:
        #     print(i)
        # print(**model_dict)
    loaded_model = Model.from_dict(model_dict)
    return loaded_model


def save_file(file_name, data):
    try:
        # Guardar la instancia en un archivo utilizando pickle
        with open(f"./models/{file_name}.pkl", "wb") as file:
            pickle.dump(data, file)
            print(f"Objeto guardado correctamente en el archivo '{file_name}.pkl'")
    except Exception as e:
        print(e)
    finally:
        file.close()

def load_file(file_name):
    try:
        with open(f"{file_name}", "rb") as file:
            data = pickle.load(file)
            print(f"Objeto cargado correctamente desde el archivo '{file_name}'")
            print(f"Nombre del objeto cargado:", data)
    except FileNotFoundError:
            print("El archivo no se encontró.")
    except EOFError:
        print("El archivo está vacío o no contiene datos válidos.")
    except Exception as e:
        print("Ocurrió un error al cargar el archivo:", e)
    return data
