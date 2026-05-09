import csv
from pathlib import Path

#  CONFIGURACION DE DATASETS 

DATASETS_CONFIG = {
    1: {
        "nombre": "IADIZA",
        "carpeta": "iadiza",
        "archivo": "occurrence.txt",
        "separador": "\t",
        "encoding": "utf-8",
    },
    2: {
        "nombre": "Xeno-canto",
        "carpeta": "xenocanto",
        "archivo": "occurrence.txt",
        "separador": ",",
        "encoding": "utf-8",
    },
    3: {
        "nombre": "iNaturalist",
        "carpeta": "inaturalist",
        "archivo": "observations.csv",
        "separador": ",",
        "encoding": "utf-8",
    }
}

#  FUNCIONES BASE         

def _obtener_ruta_proyecto() -> Path:
    """
    Obtiene la ruta raiz del proyecto.

    Que hace:
        - Parte de la ubicacion de este archivo.
        - Sube un nivel para llegar a la carpeta del proyecto.
        - Retorna la ruta al directorio raiz.
    """
    return Path(__file__).parent.parent.resolve()


def cargar_dataset(numero: int):
    """
    Devuelve la configuracion del dataset sin cargar los datos.

    Que hace:
        - Verifica que el numero sea 1, 2 o 3.
        - Busca la carpeta y archivo correcto segun la configuracion.
        - Comprueba que el archivo exista.
        - Retorna los datos necesarios para abrir el archivo mas tarde.

    Retorna:
        Un diccionario con ruta, separador, encoding y nombre del dataset.
    """
    if numero not in DATASETS_CONFIG:
        raise ValueError("El numero debe ser 1, 2 o 3")

    config = DATASETS_CONFIG[numero]
    ruta = _obtener_ruta_proyecto() / "raw_datasets" / config["carpeta"] / config["archivo"]

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontro el archivo: {ruta}")

    return {
        "ruta": ruta,
        "separador": config["separador"],
        "encoding": config["encoding"],
        "nombre": config["nombre"]
    }

# INTERFAZ (solo para notebook) 
def seleccionar_y_cargar_dataset():
    """
    Pide al usuario seleccionar uno de los datasets y retorna su configuracion.

    Que hace:
        - Muestra las opciones disponibles.
        - Lee el numero ingresado por el usuario.
        - Valida que sea 1, 2 o 3.
        - Llama a cargar_dataset() para obtener la configuracion.
        - Retorna el diccionario con la configuracion seleccionada.
    """
    while True:
        try:
            print("Seleccione el dataset a cargar:")
            print("   1 → IADIZA")
            print("   2 → Xeno-canto")
            print("   3 → iNaturalist")

            numero = int(input("\nIngrese numero (1-3): "))

            if numero in DATASETS_CONFIG:
                dataset = cargar_dataset(numero)
                print(f"\nDataset seleccionado: {dataset['nombre']}\n")
                return dataset
            else:
                print("Solo 1, 2 o 3\n")

        except ValueError:
            print("ERROR: numero invalido\n")