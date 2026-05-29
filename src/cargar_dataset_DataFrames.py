import pandas as pd
from pathlib import Path

"""
Ejercicio 1A
Se encarga de carga de datasets como DataFrames de pandas.
"""

# Configuración de datasets disponibles
DATASETS_CONFIG = {
    "IADIZA": {
        "carpeta": "iadiza",
        "archivo": "occurrence.txt",
        "separador": "\t",
        "encoding": "utf-8",
        "fuente": "processed_datasets",  # primero busca en processed, sino raw
    },
    "Xeno-canto": {
        "carpeta": "xenocanto",
        "archivo": "occurrence.txt",
        "separador": ",",
        "encoding": "utf-8",
        "fuente": "processed_datasets",
    },
    "iNaturalist": {
        "carpeta": "inaturalist",
        "archivo": "observations.csv",
        "separador": ",",
        "encoding": "utf-8",
        "fuente": "processed_datasets",
    },
}


def _obtener_ruta_proyecto():
    """Retorna la ruta raíz del proyecto."""
    return Path(__file__).parent.parent.resolve()


def _buscar_archivo(nombre_dataset: str):
    """
    Busca el archivo del dataset primero en processed_datasets, y sí
    no lo encuentra ahi, lo busca en raw_datasets.

    Returns
    -------
    tupla (ruta, separador, encoding)
    """
    if nombre_dataset not in DATASETS_CONFIG:
        raise ValueError(
            f"Dataset '{nombre_dataset}' no reconocido. "
            f"Opciones: {list(DATASETS_CONFIG.keys())}"
        )

    config = DATASETS_CONFIG[nombre_dataset]
    raiz = _obtener_ruta_proyecto()

    # Busca primero en processed_datasets
    ruta_processed = raiz / "processed_datasets" / config["carpeta"] / config["archivo"]
    if ruta_processed.exists():
        return ruta_processed, config["separador"], config["encoding"]

    # Si no existe, busca directamente el archivo (sin subcarpeta) en processed_datasets
    ruta_processed_flat = raiz / "processed_datasets" / config["archivo"]
    if ruta_processed_flat.exists():
        return ruta_processed_flat, config["separador"], config["encoding"]

    # Fallback a raw_datasets
    ruta_raw = raiz / "raw_datasets" / config["carpeta"] / config["archivo"]
    if ruta_raw.exists():
        return ruta_raw, config["separador"], config["encoding"]

    raise FileNotFoundError(
        f"No se encontró el archivo para '{nombre_dataset}'.\n"
        f"Buscado en:\n  {ruta_processed}\n  {ruta_raw}"
    )


def cargar_dataset_df(nombre_dataset: str):
    """
    Ejercicio 1A: Carga un dataset como DataFrame de pandas.
    
    Recibe el nombre del dataset, respeta el separador
    y encoding identificados en la primera entrega, y retorna el DataFrame.

    Parameters
    ----------
    nombre_dataset : str
        Nombre del dataset. Opciones: "IADIZA", "Xeno-canto", "iNaturalist".

    Returns
    -------
    pd.DataFrame
        DataFrame con todos los registros del dataset.

    Raises
    ------
    ValueError
        Si el nombre del dataset no es reconocido.
    FileNotFoundError
        Si el archivo no existe en ninguna ubicación esperada.
    """
    ruta, separador, encoding = _buscar_archivo(nombre_dataset)

    df = pd.read_csv(
        ruta,
        sep=separador,
        encoding=encoding,
        low_memory=False,
    )

    return df