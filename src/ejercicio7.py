# ================ PUNTO 7A ============================
from datetime import datetime

def obtener_fecha_hora():
    """
    Retorna la fecha y la hora actual en formato "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.now().strftime("%Y-%m-%d  %H:%M:%S")


# =============== PUNTO 7B ===============================
import os

def registrar_operacion(nombre_dataset, tipo_cambio, cantidad_registros, estado="ok"):
    """
    Registra un cambio que se realiza sobre un dataset en operations.log

    nombre_dataset: Nombre del dataset donde se realizo el cambio
    tipo_cambio: Tipo de operacion realizada (INSERT, UPDATE, DELETE)
    cantidad_registros: Cantidad de registros que se cambiaron
    estado: Estado de la operacion (OK o ERROR), por defecto OK
    """
    os.makedirs("logs", exist_ok=True)
    ruta_log = os.path.join(os.path.dirname(__file__), "..", "logs", "operations.log")

    linea = f"{obtener_fecha_hora()}  |  {nombre_dataset}  |  {tipo_cambio}  |  {cantidad_registros} registros  |  {estado}\n"

    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(linea)
    print("Operacion registrada en el log")


# ================= PUNTO 7C ==============================
import csv
from inicializar_registro import inicio_registro
from añadir_ID import preparar_para_csv
from validar_registro import agrupar_validaciones
from cargardataset import cargar_dataset

def agregar_registro_simple(numero_dataset, tipo_dataset, carpeta_destino="processed_datasets"):
    """
    Lee un dataset original, solicita un nuevo registro por teclado, lo valida y lo
    agrega al archivo en processed_datasets. Registra la operacion en el log.

    numero_dataset: Identificador del dataset a cargar
    tipo_dataset: Tipo de dataset (iadiza, xenocanto, inaturalist)
    carpeta_destino: Carpeta donde se guarda el nuevo archivo
    """
    dataset = cargar_dataset(numero_dataset)
    origen_dataset = dataset["ruta"]
    separador = dataset["separador"]

    os.makedirs(carpeta_destino, exist_ok=True)
    archivo_destino = os.path.join(carpeta_destino, os.path.basename(str(origen_dataset)))

    with open(origen_dataset, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=separador)
        encabezados = next(reader)

    registro = inicio_registro(tipo_dataset)

    for col in registro.keys():
        valor = input(f"Ingrese valor para {col}: ")
        registro[col] = valor

    errores = agrupar_validaciones(registro)
    if errores:
        print("El registro tiene errores y no puede ser insertado")
        for error in errores:
            print(" -", error)
        return

    registro = preparar_para_csv(registro, tipo_dataset)
    if "id" not in encabezados:
        encabezados.append("id")

    existe = os.path.exists(archivo_destino)
    with open(archivo_destino, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=encabezados, delimiter=separador, extrasaction="ignore")
        if not existe:
            writer.writeheader()
        writer.writerow(registro)

    # Punto 7C - Registra en el log
    registrar_operacion(os.path.basename(str(origen_dataset)), "INSERT", 1)
    print("Registro agregado correctamente")


# =================== PUNTO 7D ==========================
"""
Funcion de actualizacion fue modificada para que
    - registrar cada modificacion
    - que indique la cantidad de registros afectados
Se reutilizan las funciones que fueron creadas antes en el ejercicio 5
"""
from validacion import (
    validar_coordenadas,
    validar_fechas,
    validar_country_code,
    validar_incertidumbre_coordenadas,
    _es_nulo,
    _obtener_valor,
)

def _leer_dataset(ruta_archivo, separador="\t", encoding="utf-8"):
    """
    Lee el dataset completo en una lista de diccionarios.
    """
    with open(ruta_archivo, encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=separador)
        columnas = reader.fieldnames or []
        filas = list(reader)
    return filas, list(columnas)


def _escribir_dataset(ruta_salida, filas, columnas, separador="\t", encoding="utf-8"):
    """
    Escribe una lista de registros en un archivo CSV/TSV.
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
    """
    return _obtener_valor(fila, "occurrenceID", "id", "ID", "catalogNumber", "gbifID")


def buscar_registros(ruta_archivo, filtros, separador="\t", encoding="utf-8"):
    """
    Busca registros que coincidan con todos los filtros indicados.
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


def actualizar_campo(ruta_archivo, ruta_salida, id_registro, nombre_columna, nuevo_valor, separador="\t", encoding="utf-8"):
    """
    Actualiza el valor de un campo en el registro identificado por id_registro.
    """
    return actualizar_campos(ruta_archivo, ruta_salida, id_registro, {nombre_columna: nuevo_valor}, separador, encoding)


def actualizar_campos(ruta_archivo, ruta_salida, id_registro, cambios, separador="\t", encoding="utf-8"):
    """
    Actualiza múltiples campos de un registro en una sola operación.
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

    # == PUNTO 7D - Natalia ==
    if errores:
        registrar_operacion(os.path.basename(ruta_archivo), "UPDATE", 0, "ERROR - " + str(errores))
    else:
        registrar_operacion(os.path.basename(ruta_archivo), "UPDATE", modificados)

    return {
        "exito": len(errores) == 0,
        "registros_modificados": modificados,
        "errores": errores,
    }


def _validar_cambios(cambios, ruta_archivo, separador, encoding):
    """
    Valida los nuevos valores antes de aplicar cambios al dataset.
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
            errores.append(f"coordinateUncertaintyInMeters no es numérico: '{val_raw}'")

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


def actualizar_campo_con_validacion(ruta_archivo, ruta_salida, id_registro, nombre_columna, nuevo_valor, separador="\t", encoding="utf-8"):
    """
    Actualiza un campo validando el nuevo valor antes de aplicar el cambio.
    """
    return actualizar_campos_con_validacion(ruta_archivo, ruta_salida, id_registro, {nombre_columna: nuevo_valor}, separador, encoding)


def actualizar_campos_con_validacion(ruta_archivo, ruta_salida, id_registro, cambios, separador="\t", encoding="utf-8"):
    """
    Actualiza múltiples campos de un registro validando los nuevos valores.
    """
    errores = _validar_cambios(cambios, ruta_archivo, separador, encoding)

    if errores:
        # == PUNTO 7D - Natalia ==
        registrar_operacion(os.path.basename(ruta_archivo), "UPDATE", 0, "ERROR - " + str(errores))
        return {
            "exito": False,
            "registros_modificados": 0,
            "errores": errores,
        }

    return actualizar_campos(ruta_archivo, ruta_salida, id_registro, cambios, separador, encoding)


# ================= PUNTO 7E ==================================
def eliminar_por_id(ruta_entrada, ruta_salida, id_buscado, nombre_columna="occurrenceID", separador="\t", encoding="utf-8"):
    """
    Permite eliminar un registro específico de un dataset a partir de su identificador.
    Registra la operacion en el log.
    """
    encontrado = False
    registros_eliminados = 0

    with open(ruta_entrada, encoding=encoding) as archivo_in, \
         open(ruta_salida, "w", newline="", encoding=encoding) as archivo_out:

        lector = csv.reader(archivo_in, delimiter=separador)
        escritor = csv.writer(archivo_out, delimiter=separador)

        columnas = next(lector)
        escritor.writerow(columnas)

        try:
            indice_id = columnas.index(nombre_columna)
        except ValueError:
            print("Error: la columna especificada no existe en el dataset")
            return

        for fila in lector:
            if fila[indice_id] == id_buscado:
                encontrado = True
                registros_eliminados += 1
                continue
            escritor.writerow(fila)

    if encontrado:
        print("Registro eliminado correctamente")
        registrar_operacion(os.path.basename(ruta_entrada), "DELETE", registros_eliminados, "OK")
    else:
        print("Error: no se encontró el ID especificado")
        registrar_operacion(os.path.basename(ruta_entrada), "DELETE", 0, "ERROR - ID no encontrado")


def eliminar_por_valores(ruta_entrada, ruta_salida, columna, valores_a_eliminar, separador="\t", encoding="utf-8"):
    """
    Permite eliminar registros cuando el valor de una columna pertenece a una lista dada.
    Registra la operacion en el log.
    """
    registros_eliminados = 0

    with open(ruta_entrada, encoding=encoding) as archivo_in, \
         open(ruta_salida, "w", newline="", encoding=encoding) as archivo_out:

        lector = csv.reader(archivo_in, delimiter=separador)
        escritor = csv.writer(archivo_out, delimiter=separador)

        columnas = next(lector)
        escritor.writerow(columnas)

        try:
            indice = columnas.index(columna)
        except ValueError:
            print("Error: la columna especificada no existe en el dataset")
            registrar_operacion(os.path.basename(ruta_entrada), "DELETE", 0, "ERROR - columna no encontrada")
            return

        for fila in lector:
            if fila[indice] in valores_a_eliminar:
                registros_eliminados += 1
                continue
            escritor.writerow(fila)

    print("Filtrado completado")
    if registros_eliminados > 0:
        registrar_operacion(os.path.basename(ruta_entrada), "DELETE", registros_eliminados, "OK")
    else:
        registrar_operacion(os.path.basename(ruta_entrada), "DELETE", 0, f"ERROR - no se encontraron valores en {columna}")


def eliminar_por_condicion(ruta_entrada, ruta_salida, columna, operador, valor, separador="\t", encoding="utf-8"):
    """
    Elimina registros que cumplen una condición dada.
    Registra la operacion en el log.
    """
    registros_eliminados = 0

    def cumple_condicion(valor_fila, operador, valor):
        try:
            valor_fila = float(valor_fila)
            valor = float(valor)
        except:
            pass
        if operador == "==": return valor_fila == valor
        elif operador == "!=": return valor_fila != valor
        elif operador == ">": return valor_fila > valor
        elif operador == ">=": return valor_fila >= valor
        elif operador == "<": return valor_fila < valor
        elif operador == "<=": return valor_fila <= valor
        else:
            print("Operador no válido")
            return False

    with open(ruta_entrada, encoding=encoding) as archivo_in, \
         open(ruta_salida, "w", newline="", encoding=encoding) as archivo_out:

        lector = csv.reader(archivo_in, delimiter=separador)
        escritor = csv.writer(archivo_out, delimiter=separador)

        columnas = next(lector)
        escritor.writerow(columnas)

        try:
            indice = columnas.index(columna)
        except ValueError:
            print("Error: columna no encontrada")
            registrar_operacion(os.path.basename(ruta_entrada), "DELETE", 0, "ERROR - columna no encontrada")
            return

        for fila in lector:
            if cumple_condicion(fila[indice], operador, valor):
                registros_eliminados += 1
                continue
            escritor.writerow(fila)

    print("Filtrado por condición completado")
    if registros_eliminados > 0:
        registrar_operacion(os.path.basename(ruta_entrada), "DELETE", registros_eliminados, "OK")
    else:
        registrar_operacion(os.path.basename(ruta_entrada), "DELETE", 0, f"ERROR - no se encontraron coincidencias en {columna}")


def sanitizar_dataset(ruta_entrada, ruta_salida, separador="\t", encoding="utf-8"):
    """
    Sanitiza un dataset eliminando registros inválidos.
    Registra la operacion en el log.
    """
    total_registros = 0
    eliminados = 0
    motivos = {
        "latitud_invalida": 0,
        "longitud_invalida": 0,
        "fecha_invalida": 0,
        "nombre_cientifico_vacio": 0
    }

    with open(ruta_entrada, encoding=encoding) as archivo_in, \
         open(ruta_salida, "w", newline="", encoding=encoding) as archivo_out:

        lector = csv.reader(archivo_in, delimiter=separador)
        escritor = csv.writer(archivo_out, delimiter=separador)

        columnas = next(lector)
        escritor.writerow(columnas)

        try:
            idx_lat = columnas.index("decimalLatitude")
            idx_lon = columnas.index("decimalLongitude")
            idx_fecha = columnas.index("eventDate")
            idx_nombre = columnas.index("scientificName")
        except ValueError:
            print("Error: faltan columnas necesarias para validar")
            registrar_operacion(os.path.basename(ruta_entrada), "DELETE", 0, "ERROR - columnas faltantes")
            return

        for fila in lector:
            total_registros += 1
            eliminar = False

            if fila[idx_nombre] == "":
                motivos["nombre_cientifico_vacio"] += 1
                eliminar = True

            if fila[idx_lat] != "":
                try:
                    lat = float(fila[idx_lat])
                    if lat < -90 or lat > 90:
                        motivos["latitud_invalida"] += 1
                except:
                    motivos["latitud_invalida"] += 1

            if fila[idx_lon] != "":
                try:
                    lon = float(fila[idx_lon])
                    if lon < -180 or lon > 180:
                        motivos["longitud_invalida"] += 1
                except:
                    motivos["longitud_invalida"] += 1

            if fila[idx_fecha] == "":
                motivos["fecha_invalida"] += 1

            if eliminar:
                eliminados += 1
                continue

            escritor.writerow(fila)

    porcentaje = (eliminados / total_registros) * 100 if total_registros > 0 else 0
    print("Sanitización completada")
    print(f"Registros totales: {total_registros}")
    print(f"Registros eliminados: {eliminados}")
    print(f"Porcentaje eliminado: {porcentaje:.2f}%")
    print("Motivos detectados:")
    for motivo, cantidad in motivos.items():
        print(f"- {motivo}: {cantidad}")

    registrar_operacion(os.path.basename(ruta_entrada), "DELETE", eliminados, "OK" if eliminados > 0 else "ERROR - no se eliminaron registros")


# ========================= PUNTO 7F =======================================
def agregar_registro_con_log(numero_dataset, tipo_dataset, carpeta_destino="processed_datasets"):
    """
    Lee un dataset original, solicita un nuevo registro por teclado, lo valida y lo
    agrega al archivo en processed_datasets.

    numero_dataset: Identificador del dataset a cargar
    tipo_dataset: Tipo de dataset (iadiza, xenocanto, inaturalist)
    carpeta_destino: Carpeta donde se guarda el nuevo archivo

    1. Carga la ruta y separador del dataset original.
    2. Inicializa un registro vacío según el tipo de dataset.
    3. Pide valores por teclado para cada columna.
    4. Valida el registro con agrupar_validaciones.
        - Si hay errores → se muestran en pantalla y se registra en el log como ERROR.
        - Si no hay errores → se asigna un ID y se inserta en el archivo destino.
    5. Si el archivo destino no existe, escribe encabezados antes de insertar.
    6. Registra la operación en el log como INSERT.
    """
    dataset = cargar_dataset(numero_dataset)
    origen_dataset = dataset["ruta"]
    separador = dataset["separador"]

    os.makedirs(carpeta_destino, exist_ok=True)
    archivo_destino = os.path.join(carpeta_destino, os.path.basename(str(origen_dataset)))

    with open(origen_dataset, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=separador)
        encabezados = next(reader)

    registro = inicio_registro(tipo_dataset)

    for col in registro.keys():
        valor = input(f"Ingrese valor para {col}: ")
        registro[col] = valor

    errores = agrupar_validaciones(registro)
    if errores:
        print("El registro tiene errores y no puede ser insertado")
        for error in errores:
            print(" -", error)
        registrar_operacion(os.path.basename(str(origen_dataset)), "INSERT", 0, "ERROR - " + "; ".join(errores))
        return

    registro = preparar_para_csv(registro, tipo_dataset)
    if "id" not in encabezados:
        encabezados.append("id")

    existe = os.path.exists(archivo_destino)
    with open(archivo_destino, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=encabezados, delimiter=separador, extrasaction="ignore")
        if not existe:
            writer.writeheader()
        writer.writerow(registro)

    registrar_operacion(os.path.basename(str(origen_dataset)), "INSERT", 1)
    print("Registro agregado correctamente")