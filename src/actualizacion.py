"""
Módulo de actualización de registros en datasets Darwin Core.
Ejercicio 5 - Seminario de Lenguajes Opción Python 2026.
"""

import csv
import os

from validacion import (
    validar_coordenadas,
    validar_fechas,
    validar_country_code,
    validar_incertidumbre_coordenadas,
    _es_nulo,
    _obtener_valor,
)


# ── Utilidades internas ──────────────────────────────────────────────────────

def _leer_dataset(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Lee el dataset completo en una lista de diccionarios.

    Se usa exclusivamente para operaciones de modificación donde se
    necesita cargar el archivo completo para reescribirlo.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    tuple[list[dict], list[str]]
        (filas, nombres_de_columnas)
    """
    with open(ruta_archivo, encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=separador)
        columnas = reader.fieldnames or []
        filas = list(reader)
    return filas, list(columnas)


def _escribir_dataset(ruta_salida, filas, columnas, separador="\t", encoding="utf-8"):
    """
    Escribe una lista de registros en un archivo CSV/TSV.

    Parameters
    ----------
    ruta_salida : str
    filas : list[dict]
    columnas : list[str]
    separador : str
    encoding : str
    """
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    with open(ruta_salida, "w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=columnas, delimiter=separador, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(filas)


def _obtener_id_fila(fila):
    """
    Devuelve el valor del campo ID de una fila.

    Parameters
    ----------
    fila : dict

    Returns
    -------
    str or None
    """
    return _obtener_valor(fila, "occurrenceID", "id", "ID", "catalogNumber")


# ── Ejercicio 5.A — Búsqueda por múltiples columnas ─────────────────────────

def buscar_registros(ruta_archivo, filtros, separador="\t", encoding="utf-8"):
    """
    Busca registros que coincidan con todos los filtros indicados.

    Parameters
    ----------
    ruta_archivo : str
    filtros : dict
        Diccionario de {nombre_columna: valor_buscado}.
        Ejemplo: {"scientificName": "Elaenia chilensis", "country": "Argentina"}
    separador : str
    encoding : str

    Returns
    -------
    list[dict]
        Lista de registros que cumplen todas las condiciones.

    Examples
    --------
    >>> buscar_registros("occurrence.txt", {"occurrenceID": "1234"})
    >>> buscar_registros("occurrence.txt", {"country": "Argentina"})
    """
    resultados = []

    with open(ruta_archivo, encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=separador)
        for fila in reader:
            if all(
                str(fila.get(col, "")).strip() == str(valor).strip()
                for col, valor in filtros.items()
            ):
                resultados.append(dict(fila))

    return resultados


# ── Ejercicio 5.B — Actualizar un campo de un registro ──────────────────────

def actualizar_campo(
    ruta_archivo,
    ruta_salida,
    id_registro,
    nombre_columna,
    nuevo_valor,
    separador="\t",
    encoding="utf-8",
):
    """
    Actualiza el valor de un campo en el registro identificado por id_registro.

    Parameters
    ----------
    ruta_archivo : str
        Dataset de entrada.
    ruta_salida : str
        Dataset de salida en processed_datasets.
    id_registro : str
        Valor del campo ID del registro a modificar.
    nombre_columna : str
        Nombre del campo a actualizar.
    nuevo_valor : str
        Nuevo valor a asignar.
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "exito": bool,
            "registros_modificados": int,
            "errores": list[str]
        }
    """
    return actualizar_campos(
        ruta_archivo,
        ruta_salida,
        id_registro,
        {nombre_columna: nuevo_valor},
        separador,
        encoding,
    )


# ── Ejercicio 5.C — Actualizar múltiples campos ──────────────────────────────

def actualizar_campos(
    ruta_archivo,
    ruta_salida,
    id_registro,
    cambios,
    separador="\t",
    encoding="utf-8",
):
    """
    Actualiza múltiples campos de un registro en una sola operación.

    Parameters
    ----------
    ruta_archivo : str
        Dataset de entrada.
    ruta_salida : str
        Dataset de salida en processed_datasets.
    id_registro : str
        Valor del campo ID del registro a modificar.
    cambios : dict
        Diccionario con {nombre_columna: nuevo_valor}.
        Ejemplo: {"country": "Argentina", "stateProvince": "Buenos Aires"}
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "exito": bool,
            "registros_modificados": int,
            "errores": list[str]
        }
    """
    filas, columnas = _leer_dataset(ruta_archivo, separador, encoding)
    modificados = 0
    errores = []

    for fila in filas:
        if str(_obtener_id_fila(fila)).strip() == str(id_registro).strip():
            for col, val in cambios.items():
                if col not in columnas:
                    errores.append(f"La columna '{col}' no existe en el dataset.")
                    continue
                fila[col] = val
            modificados += 1

    if modificados == 0:
        errores.append(f"No se encontró ningún registro con ID '{id_registro}'.")

    if not errores:
        _escribir_dataset(ruta_salida, filas, columnas, separador, encoding)

    return {
        "exito": len(errores) == 0,
        "registros_modificados": modificados,
        "errores": errores,
    }


# ── Ejercicio 5.D — Actualizar con validación previa ─────────────────────────

def _validar_cambios(cambios, ruta_archivo, separador, encoding):
    """
    Valida los nuevos valores antes de aplicar cambios al dataset.

    Reutiliza las funciones de validación del módulo validacion.py
    ejecutando el dataset completo con los cambios propuestos en un
    registro temporal para detectar errores.

    Parameters
    ----------
    cambios : dict
        {nombre_columna: nuevo_valor}
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    list[str]
        Lista de errores encontrados. Vacía si todo es válido.
    """
    errores = []

    lat_raw = cambios.get("decimalLatitude") or cambios.get("latitudeDecimal")
    lon_raw = cambios.get("decimalLongitude") or cambios.get("longitudeDecimal")

    if lat_raw is not None:
        try:
            lat = float(lat_raw)
            if not -90 <= lat <= 90:
                errores.append(f"decimalLatitude fuera de rango [-90,90]: {lat}")
        except (ValueError, TypeError):
            errores.append(f"decimalLatitude no es numérico: '{lat_raw}'")

    if lon_raw is not None:
        try:
            lon = float(lon_raw)
            if not -180 <= lon <= 180:
                errores.append(f"decimalLongitude fuera de rango [-180,180]: {lon}")
        except (ValueError, TypeError):
            errores.append(f"decimalLongitude no es numérico: '{lon_raw}'")

    if "countryCode" in cambios:
        from validacion import COUNTRY_CODES_VALIDOS
        codigo = cambios["countryCode"]
        if not _es_nulo(codigo) and codigo.strip().upper() not in COUNTRY_CODES_VALIDOS:
            errores.append(f"countryCode inválido: '{codigo}'")

    if "coordinateUncertaintyInMeters" in cambios:
        val_raw = cambios["coordinateUncertaintyInMeters"]
        try:
            val = float(val_raw)
            if val < 0:
                errores.append(f"coordinateUncertaintyInMeters negativo: {val}")
            if val > 100:
                errores.append(f"coordinateUncertaintyInMeters excesivo (>100): {val}")
        except (ValueError, TypeError):
            errores.append(
                f"coordinateUncertaintyInMeters no es numérico: '{val_raw}'"
            )

    for campo, valor in cambios.items():
        if "date" in campo.lower() and not _es_nulo(valor):
            from validacion import _parsear_fecha
            from datetime import datetime
            fecha = _parsear_fecha(str(valor))
            if fecha is None:
                errores.append(f"{campo}: formato de fecha inválido ('{valor}')")
            elif fecha.year > datetime.now().year:
                errores.append(f"{campo}: fecha futura ({valor})")

    return errores


def actualizar_campo_con_validacion(
    ruta_archivo,
    ruta_salida,
    id_registro,
    nombre_columna,
    nuevo_valor,
    separador="\t",
    encoding="utf-8",
):
    """
    Actualiza un campo validando el nuevo valor antes de aplicar el cambio.

    Parameters
    ----------
    ruta_archivo : str
    ruta_salida : str
    id_registro : str
    nombre_columna : str
    nuevo_valor : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "exito": bool,
            "registros_modificados": int,
            "errores": list[str]
        }
    """
    return actualizar_campos_con_validacion(
        ruta_archivo,
        ruta_salida,
        id_registro,
        {nombre_columna: nuevo_valor},
        separador,
        encoding,
    )


def actualizar_campos_con_validacion(
    ruta_archivo,
    ruta_salida,
    id_registro,
    cambios,
    separador="\t",
    encoding="utf-8",
):
    """
    Actualiza múltiples campos de un registro validando los nuevos valores.

    Si alguna validación falla el registro NO se modifica y se reportan
    los errores encontrados.

    Parameters
    ----------
    ruta_archivo : str
        Dataset de entrada.
    ruta_salida : str
        Dataset de salida en processed_datasets.
    id_registro : str
        Valor del campo ID del registro a modificar.
    cambios : dict
        {nombre_columna: nuevo_valor}
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "exito": bool,
            "registros_modificados": int,
            "errores": list[str]
        }
    """
    errores = _validar_cambios(cambios, ruta_archivo, separador, encoding)

    if errores:
        return {
            "exito": False,
            "registros_modificados": 0,
            "errores": errores,
        }

    return actualizar_campos(
        ruta_archivo,
        ruta_salida,
        id_registro,
        cambios,
        separador,
        encoding,
    )
