import csv

# AUXILIAR


def _abrir_dataset(dataset):
    """
    Abre el archivo del dataset con la codificacion y separador correctos.

    Parametros:
        dataset: Diccionario con los datos de configuracion del dataset.

    Que hace:
        - Usa la ruta, el encoding y el separador definidos en el diccionario.
        - Devuelve el archivo abierto para que csv.DictReader pueda leerlo.
    """
    return open(dataset["ruta"], encoding=dataset["encoding"], newline="")


def _obtener_columnas(dataset):
    """
    Lee la primera fila del dataset y obtiene los nombres de columnas.

    Que hace:
        - Abre el archivo con _abrir_dataset().
        - Usa csv.DictReader para leer los encabezados.
        - Retorna los nombres de las columnas en una lista.
    """
    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])
        return reader.fieldnames


# ====================== EJERCICIO 2.A ======================
def ejercicio2A(dataset):
    """
    Muestra las primeras 10 filas del dataset.

    Que hace:
        - Abre el archivo con csv.DictReader.
        - Recorre fila por fila hasta 10 registros.
        - Imprime cada fila como un diccionario.

    Retorna:
        None.
    """
    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])
        for i, fila in enumerate(reader):
            if i >= 10:
                break
            print(fila)


# ====================== EJERCICIO 2.B ======================
def ejercicio2B(dataset):
    """
    Retorna la lista de nombres de columnas del archivo.

    Que hace:
        - Obtiene el encabezado del archivo.
        - Retorna los nombres de columna en el orden en que aparecen.
    """
    return _obtener_columnas(dataset)


# ====================== EJERCICIO 2.C ======================
def ejercicio2C(dataset):
    """
    Retorna la posicion de cada columna comenzando en 1.

    Que hace:
        - Obtiene los nombres de columnas.
        - Crea un diccionario con columna:posicion.
    """
    columnas = _obtener_columnas(dataset)
    return {col: i + 1 for i, col in enumerate(columnas)}


# ====================== EJERCICIO 2.D ======================
def ejercicio2D(dataset):
    """
    Cuenta la cantidad total de registros del dataset.

    Que hace:
        - Recorre todas las filas del archivo con csv.DictReader.
        - Suma una unidad por cada fila leida.

    Retorna:
        El numero total de registros.
    """
    total = 0
    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])
        for _ in reader:
            total += 1
    return total


# ====================== EJERCICIO 2.E ======================
def ejercicio2E(dataset):
    """
    Detecta que columnas tienen al menos un valor nulo o vacio.

    Que hace:
        - Recorre cada fila del archivo.
        - Marca la columna cuando encuentra un dato faltante.
        - Evita duplicados usando un set.

    Retorna:
        Una lista de columnas con datos nulos.
    """
    columnas = _obtener_columnas(dataset)
    nulas = set()

    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])
        for fila in reader:
            for col in columnas:
                val = fila.get(col)
                if val is None or val.strip() == "":
                    nulas.add(col)

    return list(nulas)


# ====================== EJERCICIO 2.F ======================
def ejercicio2F(dataset):
    """
    Calcula el porcentaje de valores nulos por columna.

    Que hace:
        - Cuenta cuantos valores vacios tiene cada columna.
        - Calcula el porcentaje respecto al total de registros.

    Retorna:
        Un diccionario con el porcentaje de nulos por columna.
    """
    columnas = _obtener_columnas(dataset)
    conteo = {col: 0 for col in columnas}
    total = 0

    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])
        for fila in reader:
            total += 1
            for col in columnas:
                val = fila.get(col)
                if val is None or val.strip() == "":
                    conteo[col] += 1

    if total == 0:
        return {"error": "El dataset esta vacio"}

    return {col: round((conteo[col] / total) * 100, 2) for col in columnas}


# ====================== EJERCICIO 2.G ======================
def ejercicio2G(dataset, columna):
    """
    Cuenta cuantos valores distintos hay en una columna.

    Que hace:
        - Verifica que la columna exista.
        - Usa un set para guardar valores unicos.
        - Trata los valores vacios como "NULL".

    Retorna:
        La cantidad de valores distintos.
    """
    columnas = _obtener_columnas(dataset)

    if columna not in columnas:
        return {"error": f"La columna '{columna}' no existe"}

    valores = set()

    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])
        for fila in reader:
            val = fila.get(columna)
            if val is None or val.strip() == "":
                valores.add("NULL")
            else:
                valores.add(val.strip())

    return len(valores)


# ====================== EJERCICIO 2.H ======================
def ejercicio2H(dataset, columna):
    """
    Calcula la frecuencia de cada valor en una columna.

    Que hace:
        - Verifica que la columna exista.
        - Recorre cada fila y cuenta cada valor distinto.
        - Usa un diccionario donde la clave es el valor y el valor es la cantidad.

    Retorna:
        Un diccionario de frecuencias.
    """
    columnas = _obtener_columnas(dataset)

    if columna not in columnas:
        return {"error": f"La columna '{columna}' no existe"}

    frecuencia = {}

    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])
        for fila in reader:
            val = fila.get(columna)

            if val is None or val.strip() == "":
                clave = "NULL"
            else:
                clave = val.strip()

            frecuencia[clave] = frecuencia.get(clave, 0) + 1

    return frecuencia


# ====================== EJERCICIO 2.I ======================
def ejercicio2I(dataset, columna, tipo):
    """
    Analiza una columna segun su tipo y retorna estadisticas basicas.

    Que hace:
        - Verifica que la columna exista.
        - Reune los valores no vacios de la columna.
        - Segun el tipo, calcula estadisticas especificas.

    Retorna:
        Un diccionario con las estadisticas correspondientes al tipo.
    """
    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])

        if columna not in reader.fieldnames:
            return {"error": f"La columna '{columna}' no existe"}

        valores = []
        for fila in reader:
            val = fila.get(columna)
            if val is not None and val.strip() != "":
                valores.append(val.strip())

        if not valores:
            return {"error": f"No hay datos validos en '{columna}'"}

        # NUMERIC
        if tipo == "numeric":
            nums = []
            for v in valores:
                try:
                    nums.append(float(v))
                except ValueError:
                    continue

            if not nums:
                return {"error": f"No hay valores numericos en '{columna}'"}

            return {
                "min": min(nums),
                "max": max(nums),
                "promedio": sum(nums) / len(nums),
            }

        # COORDINATE
        elif tipo == "coordinate":
            nums = []
            for v in valores:
                try:
                    nums.append(float(v))
                except ValueError:
                    continue

            if not nums:
                return {"error": f"No hay coordenadas validas en '{columna}'"}

            return {"min": min(nums), "max": max(nums)}

        # TEXT
        elif tipo == "text":
            largos = [len(v) for v in valores]
            return {"min": min(largos), "max": max(largos)}

        else:
            return {"error": "Tipo invalido (usar numeric, coordinate o text)"}


# ====================== EJERCICIO 2.J ======================
def ejercicio2J(dataset):
    """
    Identifica columnas que estan completamente vacias.

    Que hace:
        - Obtiene el listado de columnas.
        - Recorre todas las filas y cuenta valores vacios por columna.
        - Compara el total de nulos con el total de registros.

    Retorna:
        Un diccionario con la lista de columnas vacias.
    """
    columnas = _obtener_columnas(dataset)

    if not columnas:
        return {"error": "No se pudieron obtener columnas"}

    conteo = {col: 0 for col in columnas}
    total = 0

    with _abrir_dataset(dataset) as f:
        reader = csv.DictReader(f, delimiter=dataset["separador"])
        for fila in reader:
            total += 1
            for col in columnas:
                val = fila.get(col)
                if val is None or val.strip() == "":
                    conteo[col] += 1

    if total == 0:
        return {"error": "El dataset esta vacio"}

    vacias = [col for col in columnas if conteo[col] == total]

    return {"columnas_vacias": vacias}
