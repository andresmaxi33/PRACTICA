import csv


def eliminar_por_id(ruta_entrada, ruta_salida, id_buscado, nombre_columna="occurrenceID", separador="\t", encoding="utf-8"):
    """
    Esta función permite eliminar un registro específico de un dataset a partir de su identificador.

    Se espera que:
    - El archivo de entrada sea un dataset estructurado (por ejemplo, Darwin Core).
    - Exista una columna identificadora (por defecto "occurrenceID").
    - Se proporcione el ID del registro que se desea eliminar.

    Qué hace la función:
    - Abre el dataset original en modo lectura.
    - Crea un nuevo archivo en la carpeta processed_datasets.
    - Copia todos los registros excepto aquel que coincide con el ID buscado.
    - Si el ID no se encuentra, informa un error.
    
    Importante:
    - No modifica el archivo original.
    - Trabaja de forma secuencial (no carga todo en memoria).
    """

    encontrado = False

    # Abrimos archivo de entrada (lectura) y salida (escritura)
    with open(ruta_entrada, encoding=encoding) as archivo_in, \
         open(ruta_salida, "w", newline="", encoding=encoding) as archivo_out:

        lector = csv.reader(archivo_in, delimiter=separador)
        escritor = csv.writer(archivo_out, delimiter=separador)

        # Leemos encabezado y lo copiamos al nuevo archivo
        columnas = next(lector)
        escritor.writerow(columnas)

        # Buscamos la posición de la columna que contiene el ID
        try:
            indice_id = columnas.index(nombre_columna)
        except ValueError:
            print("Error: la columna especificada no existe en el dataset")
            return

        # Recorremos el dataset fila por fila
        for fila in lector:

            # Si encontramos el registro, no lo copiamos (lo eliminamos)
            if fila[indice_id] == id_buscado:
                encontrado = True
                continue

            # Copiamos el resto de los registros
            escritor.writerow(fila)

    # Mensaje final según resultado
    if encontrado:
        print("Registro eliminado correctamente")
    else:
        print("Error: no se encontró el ID especificado")


def eliminar_por_valores(ruta_entrada, ruta_salida, columna, valores_a_eliminar, separador="\t", encoding="utf-8"):
    """
    Permite eliminar registros de un dataset cuando el valor de una columna
    pertenece a una lista de valores dada por el usuario.

    Se espera:
    - Una columna válida dentro del dataset
    - Una lista de valores a eliminar (por ejemplo países, códigos, etc.)

    Qué hace:
    - Lee el dataset original de forma secuencial
    - Filtra los registros que coinciden con los valores indicados
    - Genera un nuevo archivo sin modificar el original

    Este tipo de filtrado es útil para limpiar datos o acotar el análisis
    a ciertos subconjuntos de interés.
    """

    # Abrimos el archivo original y creamos uno nuevo para guardar el resultado
    with open(ruta_entrada, encoding=encoding) as archivo_in, \
         open(ruta_salida, "w", newline="", encoding=encoding) as archivo_out:

        lector = csv.reader(archivo_in, delimiter=separador)
        escritor = csv.writer(archivo_out, delimiter=separador)

        # Leemos la fila de encabezados (nombres de columnas)
        columnas = next(lector)
        escritor.writerow(columnas)

        # Buscamos la posición de la columna indicada
        try:
            indice = columnas.index(columna)
        except ValueError:
            print("Error: la columna especificada no existe en el dataset")
            return

        # Recorremos el dataset fila por fila
        for fila in lector:

            # Si el valor de la columna está en la lista, se elimina (no se copia)
            if fila[indice] in valores_a_eliminar:
                continue

            # En caso contrario, el registro se mantiene
            escritor.writerow(fila)

    # Mensaje final indicando que el proceso terminó
    print("Filtrado completado")


def eliminar_por_condicion(ruta_entrada, ruta_salida, columna, operador, valor, separador="\t", encoding="utf-8"):
    """
    Elimina registros que cumplen una condición dada por el usuario.

    Se espera:
    - Una columna válida del dataset
    - Un operador de comparación (==, !=, >, >=, <, <=)
    - Un valor contra el cual comparar

    Qué hace:
    - Lee el dataset original
    - Evalúa la condición para cada registro
    - Elimina aquellos que cumplen la condición
    - Genera un nuevo archivo sin modificar el original
    """

    # Función auxiliar para evaluar condiciones
    def cumple_condicion(valor_fila, operador, valor):
        try:
            # Intentamos comparar como números
            valor_fila = float(valor_fila)
            valor = float(valor)
        except:
            # Si falla, se comparan como strings
            pass

        if operador == "==":
            return valor_fila == valor
        elif operador == "!=":
            return valor_fila != valor
        elif operador == ">":
            return valor_fila > valor
        elif operador == ">=":
            return valor_fila >= valor
        elif operador == "<":
            return valor_fila < valor
        elif operador == "<=":
            return valor_fila <= valor
        else:
            print("Operador no válido")
            return False


    # Apertura de archivos
    with open(ruta_entrada, encoding=encoding) as archivo_in, \
         open(ruta_salida, "w", newline="", encoding=encoding) as archivo_out:

        lector = csv.reader(archivo_in, delimiter=separador)
        escritor = csv.writer(archivo_out, delimiter=separador)

        columnas = next(lector)
        escritor.writerow(columnas)

        # Buscar índice de columna
        try:
            indice = columnas.index(columna)
        except ValueError:
            print("Error: columna no encontrada")
            return

        # Recorrido del dataset
        for fila in lector:

            # Si cumple la condición → se elimina
            if cumple_condicion(fila[indice], operador, valor):
                continue

            escritor.writerow(fila)

    print("Filtrado por condición completado")


def sanitizar_dataset(ruta_entrada, ruta_salida, separador="\t", encoding="utf-8"):
    """
    Sanitiza un dataset eliminando registros inválidos.

    Criterios aplicados:
    - Se elimina solo si falta el nombre científico (campo obligatorio)
    - Latitud y longitud se validan solo si están presentes
    - Fecha se registra como problema pero no elimina registros

    Genera:
    - Nuevo dataset limpio en processed_datasets
    - Reporte de calidad (cantidad, porcentaje y motivos)
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

        # Índices de columnas necesarias
        try:
            idx_lat = columnas.index("decimalLatitude")
            idx_lon = columnas.index("decimalLongitude")
            idx_fecha = columnas.index("eventDate")
            idx_nombre = columnas.index("scientificName")
        except ValueError:
            print("Error: faltan columnas necesarias para validar")
            return

        for fila in lector:
            total_registros += 1
            eliminar = False

            # 🔴 VALIDACIÓN CRÍTICA (sí elimina)
            if fila[idx_nombre] == "":
                motivos["nombre_cientifico_vacio"] += 1
                eliminar = True

            # 🟡 VALIDACIONES NO CRÍTICAS (solo informan)

            # Latitud
            if fila[idx_lat] != "":
                try:
                    lat = float(fila[idx_lat])
                    if lat < -90 or lat > 90:
                        motivos["latitud_invalida"] += 1
                except:
                    motivos["latitud_invalida"] += 1

            # Longitud
            if fila[idx_lon] != "":
                try:
                    lon = float(fila[idx_lon])
                    if lon < -180 or lon > 180:
                        motivos["longitud_invalida"] += 1
                except:
                    motivos["longitud_invalida"] += 1

            # Fecha (NO elimina)
            if fila[idx_fecha] == "":
                motivos["fecha_invalida"] += 1

            # Decisión final
            if eliminar:
                eliminados += 1
                continue

            escritor.writerow(fila)

    porcentaje = (eliminados / total_registros) * 100 if total_registros > 0 else 0

    # Reporte final
    print("Sanitización completada")
    print(f"Registros totales: {total_registros}")
    print(f"Registros eliminados: {eliminados}")
    print(f"Porcentaje eliminado: {porcentaje:.2f}%")
    print("Motivos detectados:")

    for motivo, cantidad in motivos.items():
        print(f"- {motivo}: {cantidad}")