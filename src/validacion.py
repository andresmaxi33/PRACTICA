"""
Módulo de validación y calidad de datos Darwin Core.
Ejercicio 3 - Seminario de Lenguajes Opción Python 2026.
"""

import csv
from datetime import datetime

# ── Constantes de cobertura geográfica (Ejercicio 3.H) ──────────────────────
# Cotas aproximadas para América del Sur
LATITUD_MIN_AS = -56.0
LATITUD_MAX_AS = 13.0
LONGITUD_MIN_AS = -82.0
LONGITUD_MAX_AS = -34.0

# Códigos de país ISO 3166-1 alpha-2 válidos (muestra representativa)
COUNTRY_CODES_VALIDOS = {
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT",
    "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI",
    "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY",
    "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN",
    "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM",
    "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK",
    "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL",
    "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM",
    "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR",
    "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN",
    "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS",
    "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK",
    "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW",
    "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP",
    "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM",
    "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW",
    "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM",
    "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF",
    "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW",
    "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI",
    "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW",
}

# Formatos de fecha aceptados
FORMATOS_FECHA = [
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y/%m/%d",
    "%d/%m/%Y",
    "%Y",
]


# ── Utilidades internas ──────────────────────────────────────────────────────

def _abrir_dataset(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Abre un archivo CSV/TSV como iterador de filas (DictReader).

    Parameters
    ----------
    ruta_archivo : str
        Ruta al archivo.
    separador : str
        Separador de campos.
    encoding : str
        Codificación del archivo.

    Yields
    ------
    dict
        Cada fila del archivo como diccionario.
    """
    with open(ruta_archivo, encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=separador)
        yield from reader


def _obtener_valor(fila, *nombres_posibles):
    """
    Devuelve el valor de la primera clave encontrada en la fila.

    Parameters
    ----------
    fila : dict
        Fila del dataset.
    *nombres_posibles : str
        Nombres alternativos de la columna.

    Returns
    -------
    str or None
    """
    for nombre in nombres_posibles:
        if nombre in fila:
            return fila[nombre]
    return None


def _intentar_float(valor):
    """
    Intenta convertir un valor a float.

    Parameters
    ----------
    valor : str

    Returns
    -------
    tuple[bool, float or None]
        (éxito, valor_float)
    """
    try:
        return True, float(valor)
    except (ValueError, TypeError):
        return False, None


def _es_nulo(valor):
    """
    Determina si un valor se considera nulo o vacío.

    Parameters
    ----------
    valor : str or None

    Returns
    -------
    bool
    """
    return valor is None or str(valor).strip() == ""


# ── Ejercicio 3.A — Validación de coordenadas ───────────────────────────────

def validar_coordenadas(
    ruta_archivo, separador="\t", encoding="utf-8"
):
    """
    Detecta registros con coordenadas geográficas inválidas.

    Verifica que decimalLatitude esté en [-90, 90],
    decimalLongitude en [-180, 180] y que ambos sean numéricos.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "cantidad_invalidos": int,
            "registros_invalidos": list[dict]
        }
    """
    invalidos = []

    for fila in _abrir_dataset(ruta_archivo, separador, encoding):
        lat_raw = _obtener_valor(fila, "decimalLatitude", "latitudeDecimal")
        lon_raw = _obtener_valor(fila, "decimalLongitude", "longitudeDecimal")

        lat_ok, lat = _intentar_float(lat_raw)
        lon_ok, lon = _intentar_float(lon_raw)

        motivos = []
        if not lat_ok:
            motivos.append(f"latitud no numérica: '{lat_raw}'")
        elif lat < -90 or lat > 90:
            motivos.append(f"latitud fuera de rango: {lat}")

        if not lon_ok:
            motivos.append(f"longitud no numérica: '{lon_raw}'")
        elif lon < -180 or lon > 180:
            motivos.append(f"longitud fuera de rango: {lon}")

        if motivos:
            invalidos.append({**fila, "_motivos": motivos})

    return {
        "cantidad_invalidos": len(invalidos),
        "registros_invalidos": invalidos,
    }


# ── Ejercicio 3.B — Coordenadas incompletas ─────────────────────────────────

def validar_coordenadas_incompletas(
    ruta_archivo, separador="\t", encoding="utf-8"
):
    """
    Detecta registros donde solo una de las coordenadas está presente.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "cantidad": int,
            "registros": list[dict]
        }
    """
    incompletos = []

    for fila in _abrir_dataset(ruta_archivo, separador, encoding):
        lat = _obtener_valor(fila, "decimalLatitude", "latitudeDecimal")
        lon = _obtener_valor(fila, "decimalLongitude", "longitudeDecimal")

        tiene_lat = not _es_nulo(lat)
        tiene_lon = not _es_nulo(lon)

        if tiene_lat != tiene_lon:
            motivo = "tiene latitud pero no longitud" if tiene_lat else "tiene longitud pero no latitud"
            incompletos.append({**fila, "_motivo": motivo})

    return {"cantidad": len(incompletos), "registros": incompletos}


# ── Ejercicio 3.C — Validación de fechas ────────────────────────────────────

def _parsear_fecha(valor):
    """
    Intenta interpretar una cadena como fecha con los formatos aceptados.

    Parameters
    ----------
    valor : str

    Returns
    -------
    datetime or None
    """
    for fmt in FORMATOS_FECHA:
        try:
            return datetime.strptime(valor.strip(), fmt)
        except (ValueError, AttributeError):
            continue
    return None


def validar_fechas(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Detecta registros con fechas inválidas o posteriores al año actual.

    Aplica validación a todos los campos que contengan 'date' o 'Date'
    en su nombre.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "cantidad_invalidos": int,
            "registros_invalidos": list[dict]
        }
    """
    invalidos = []
    anio_actual = datetime.now().year

    for fila in _abrir_dataset(ruta_archivo, separador, encoding):
        campos_fecha = [k for k in fila if "date" in k.lower()]
        motivos = []

        for campo in campos_fecha:
            valor = fila.get(campo, "")
            if _es_nulo(valor):
                continue

            fecha = _parsear_fecha(valor)
            if fecha is None:
                motivos.append(f"{campo}: formato inválido ('{valor}')")
            elif fecha.year > anio_actual:
                motivos.append(f"{campo}: fecha futura ({valor})")

        if motivos:
            invalidos.append({**fila, "_motivos": motivos})

    return {
        "cantidad_invalidos": len(invalidos),
        "registros_invalidos": invalidos,
    }


# ── Ejercicio 3.D — Registros duplicados ────────────────────────────────────

def detectar_duplicados(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Detecta registros duplicados usando el campo de ID del dataset.

    Busca columnas como occurrenceID, id, ID o similar.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "cantidad_duplicados": int,
            "ids_repetidos": dict  {id: count}
        }
    """
    conteos = {}

    for fila in _abrir_dataset(ruta_archivo, separador, encoding):
        id_val = _obtener_valor(fila, "occurrenceID", "id", "ID", "catalogNumber")
        if id_val is None:
            continue
        conteos[id_val] = conteos.get(id_val, 0) + 1

    ids_repetidos = {k: v for k, v in conteos.items() if v > 1}

    return {
        "cantidad_duplicados": sum(v - 1 for v in ids_repetidos.values()),
        "ids_repetidos": ids_repetidos,
    }


# ── Ejercicio 3.E — Validación de countryCode ───────────────────────────────

def validar_country_code(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Detecta valores no permitidos en el campo countryCode.

    Los valores válidos son códigos ISO 3166-1 alpha-2.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "cantidad_invalidos": int,
            "registros_invalidos": list[dict]
        }
    """
    invalidos = []

    for fila in _abrir_dataset(ruta_archivo, separador, encoding):
        codigo = _obtener_valor(fila, "countryCode")
        if _es_nulo(codigo):
            continue
        if codigo.strip().upper() not in COUNTRY_CODES_VALIDOS:
            invalidos.append({**fila, "_motivo": f"countryCode inválido: '{codigo}'"})

    return {
        "cantidad_invalidos": len(invalidos),
        "registros_invalidos": invalidos,
    }


# ── Ejercicio 3.F — Validación de coordinateUncertaintyInMeters ─────────────

def validar_incertidumbre_coordenadas(
    ruta_archivo, umbral_maximo=100, separador="\t", encoding="utf-8"
):
    """
    Detecta valores inválidos en coordinateUncertaintyInMeters.

    Considera inválido si: no es numérico, es negativo o supera umbral_maximo.

    Parameters
    ----------
    ruta_archivo : str
    umbral_maximo : float
        Valor máximo aceptado (por defecto 100).
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "cantidad_invalidos": int,
            "registros_invalidos": list[dict]
        }
    """
    invalidos = []

    for fila in _abrir_dataset(ruta_archivo, separador, encoding):
        valor_raw = _obtener_valor(fila, "coordinateUncertaintyInMeters")
        if _es_nulo(valor_raw):
            continue

        ok, valor = _intentar_float(valor_raw)
        motivos = []

        if not ok:
            motivos.append(f"no numérico: '{valor_raw}'")
        else:
            if valor < 0:
                motivos.append(f"valor negativo: {valor}")
            if valor > umbral_maximo:
                motivos.append(f"valor excesivo (>{umbral_maximo}): {valor}")

        if motivos:
            invalidos.append({**fila, "_motivos": motivos})

    return {
        "cantidad_invalidos": len(invalidos),
        "registros_invalidos": invalidos,
    }


# ── Ejercicio 3.G — Resumen de calidad ──────────────────────────────────────

def resumen_calidad(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Genera un resumen de calidad del dataset.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    tuple[dict, str]
        (diccionario_resumen, reporte_texto)
    """
    total = 0
    sin_taxon = 0

    for fila in _abrir_dataset(ruta_archivo, separador, encoding):
        total += 1
        nombre = _obtener_valor(
            fila, "scientificName", "taxonName", "species", "genus"
        )
        if _es_nulo(nombre):
            sin_taxon += 1

    coords = validar_coordenadas(ruta_archivo, separador, encoding)
    fechas = validar_fechas(ruta_archivo, separador, encoding)
    dupes = detectar_duplicados(ruta_archivo, separador, encoding)

    resumen = {
        "total_registros": total,
        "coordenadas_invalidas": coords["cantidad_invalidos"],
        "fechas_invalidas": fechas["cantidad_invalidos"],
        "registros_duplicados": dupes["cantidad_duplicados"],
        "taxon_incompleto": sin_taxon,
    }

    reporte = (
        f"=== Reporte de Calidad del Dataset ===\n"
        f"Archivo              : {ruta_archivo}\n"
        f"Total de registros   : {total}\n"
        f"Coordenadas inválidas: {coords['cantidad_invalidos']}\n"
        f"Fechas inválidas     : {fechas['cantidad_invalidos']}\n"
        f"Registros duplicados : {dupes['cantidad_duplicados']}\n"
        f"Taxón incompleto     : {sin_taxon}\n"
        f"======================================\n"
    )

    return resumen, reporte


# ── Ejercicio 3.H — Validación por cotas de América del Sur ─────────────────

def validar_coordenadas_america_sur(
    ruta_archivo, separador="\t", encoding="utf-8"
):
    """
    Valida que las coordenadas se encuentren dentro de América del Sur.

    Utiliza las constantes LATITUD_MIN_AS, LATITUD_MAX_AS,
    LONGITUD_MIN_AS, LONGITUD_MAX_AS.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        {
            "cantidad_fuera": int,
            "registros_fuera": list[dict]
        }
    """
    fuera = []

    for fila in _abrir_dataset(ruta_archivo, separador, encoding):
        lat_raw = _obtener_valor(fila, "decimalLatitude", "latitudeDecimal")
        lon_raw = _obtener_valor(fila, "decimalLongitude", "longitudeDecimal")

        if _es_nulo(lat_raw) or _es_nulo(lon_raw):
            continue

        lat_ok, lat = _intentar_float(lat_raw)
        lon_ok, lon = _intentar_float(lon_raw)

        if not lat_ok or not lon_ok:
            continue

        motivos = []
        if not (LATITUD_MIN_AS <= lat <= LATITUD_MAX_AS):
            motivos.append(
                f"latitud fuera de AS: {lat} "
                f"(rango [{LATITUD_MIN_AS}, {LATITUD_MAX_AS}])"
            )
        if not (LONGITUD_MIN_AS <= lon <= LONGITUD_MAX_AS):
            motivos.append(
                f"longitud fuera de AS: {lon} "
                f"(rango [{LONGITUD_MIN_AS}, {LONGITUD_MAX_AS}])"
            )

        if motivos:
            fuera.append({**fila, "_motivos": motivos})

    return {"cantidad_fuera": len(fuera), "registros_fuera": fuera}


# ── Ejercicio 3.I — Validaciones agrupadas por campo ────────────────────────

def validar_latitud(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Ejecuta todas las validaciones aplicables al campo de latitud.

    Incluye: rango global [-90,90], cotas América del Sur y
    consistencia con longitud.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        Resultados combinados de todas las validaciones de latitud.
    """
    coords_globales = validar_coordenadas(ruta_archivo, separador, encoding)
    coords_as = validar_coordenadas_america_sur(ruta_archivo, separador, encoding)
    coords_incompletas = validar_coordenadas_incompletas(ruta_archivo, separador, encoding)

    # Filtrar solo registros con error en latitud
    invalidos_lat = [
        r for r in coords_globales["registros_invalidos"]
        if any("latitud" in m for m in r.get("_motivos", []))
    ]

    return {
        "invalidos_rango_global": len(invalidos_lat),
        "registros_invalidos_rango_global": invalidos_lat,
        "fuera_america_sur": coords_as["cantidad_fuera"],
        "registros_fuera_america_sur": coords_as["registros_fuera"],
        "con_latitud_sin_longitud": sum(
            1 for r in coords_incompletas["registros"]
            if "latitud" in r.get("_motivo", "")
        ),
    }


def validar_longitud(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Ejecuta todas las validaciones aplicables al campo de longitud.

    Incluye: rango global [-180,180], cotas América del Sur y
    consistencia con latitud.

    Parameters
    ----------
    ruta_archivo : str
    separador : str
    encoding : str

    Returns
    -------
    dict
        Resultados combinados de todas las validaciones de longitud.
    """
    coords_globales = validar_coordenadas(ruta_archivo, separador, encoding)
    coords_as = validar_coordenadas_america_sur(ruta_archivo, separador, encoding)
    coords_incompletas = validar_coordenadas_incompletas(ruta_archivo, separador, encoding)

    invalidos_lon = [
        r for r in coords_globales["registros_invalidos"]
        if any("longitud" in m for m in r.get("_motivos", []))
    ]

    return {
        "invalidos_rango_global": len(invalidos_lon),
        "registros_invalidos_rango_global": invalidos_lon,
        "fuera_america_sur": coords_as["cantidad_fuera"],
        "registros_fuera_america_sur": coords_as["registros_fuera"],
        "con_longitud_sin_latitud": sum(
            1 for r in coords_incompletas["registros"]
            if "longitud" in r.get("_motivo", "")
        ),
    }


# ── Validaciones por registro (auxiliares para ejercicio 4/5) ────────────────

def validar_latitud_registro(valor):
    """
    Valida un valor de latitud individual.

    Parameters
    ----------
    valor : str

    Returns
    -------
    list[str]
        Lista de errores encontrados (vacía si es válido).
    """
    errores = []
    try:
        lat = float(valor)
        if lat < -90 or lat > 90:
            errores.append("Latitud fuera de rango [-90,90]")
        if lat < -56 or lat > 13:
            errores.append("Latitud fuera de Sudamérica [-56,13]")
    except (ValueError, TypeError):
        errores.append("Latitud no numérica")
    return errores


def validar_longitud_registro(valor):
    """
    Valida un valor de longitud individual.

    Parameters
    ----------
    valor : str

    Returns
    -------
    list[str]
        Lista de errores encontrados (vacía si es válido).
    """
    errores = []
    try:
        lon = float(valor)
        if lon < -180 or lon > 180:
            errores.append("Longitud fuera de rango [-180,180]")
        if lon < -82 or lon > -34:
            errores.append("Longitud fuera de Sudamérica [-82,-34]")
    except (ValueError, TypeError):
        errores.append("Longitud no numérica")
    return errores


def validar_fecha_registro(valor):
    """
    Valida un valor de fecha individual.

    Parameters
    ----------
    valor : str or None

    Returns
    -------
    list[str]
        Lista de errores encontrados (vacía si es válido).
    """
    errores = []
    if valor is None or str(valor).strip() == "":
        return errores
    fecha = _parsear_fecha(str(valor).strip())
    if fecha is None:
        errores.append(f"Fecha inválida: {valor}")
    elif fecha.year > datetime.now().year:
        errores.append(f"Fecha futura: {valor}")
    return errores


def validar_countryCode_registro(valor):
    """
    Valida un valor de countryCode individual.

    Parameters
    ----------
    valor : str or None

    Returns
    -------
    list[str]
        Lista de errores encontrados (vacía si es válido).
    """
    errores = []
    if valor is None or str(valor).strip() == "":
        return errores
    if valor.strip().upper() not in COUNTRY_CODES_VALIDOS:
        errores.append(f"CountryCode inválido: {valor}")
    return errores


def validar_incertidumbre_registro(valor, umbral=100):
    """
    Valida un valor de coordinateUncertaintyInMeters individual.

    Parameters
    ----------
    valor : str or None
    umbral : float
        Valor máximo aceptado (por defecto 100).

    Returns
    -------
    list[str]
        Lista de errores encontrados (vacía si es válido).
    """
    errores = []
    if valor is None or str(valor).strip() == "":
        return errores
    try:
        inc = float(valor)
        if inc < 0:
            errores.append("Incertidumbre negativa")
        if inc > umbral:
            errores.append(f"Incertidumbre mayor a {umbral}")
    except (ValueError, TypeError):
        errores.append(f"Incertidumbre no numérica: {valor}")
    return errores
