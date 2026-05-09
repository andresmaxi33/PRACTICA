#===================== Punto 4A =======================
def inicio_registro (tipo_dataset):
    """
        Crea un diccionario que representa el registro vacio
        segun el tipo de dataset

        Segun el tipo de dataset va a tener ciertos datos

        Devuelve el diccionario inicializado con valores vacio "" o 0.0

        Se devuelve ValueError si el tipo de dataset no es ninguno de los tres
    """
    #Datos en comun de los tres registros
    #Campos de iadiza y xenocanto pero no de inaturalist
    if tipo_dataset == "iadiza" or tipo_dataset == "xenocanto":
        nuevo_registro = {
            "scientificName": "",
            "decimalLatitude": 0.0,
            "decimalLongitude": 0.0,
            "basisOfRecord": "",
            "eventDate": "",
            "country": "",
            "recordedBy": ""
        }

        if tipo_dataset == "iadiza":
            #Registro para archivos iadiza
            nuevo_registro.update({
                "kingdom": "",
                "phylum": "",
                "class": "",
                "order": "", 
                "family": "",
                "genus": "",
                "stateProvince": "",
            })

        elif tipo_dataset == "xenocanto":
            #Registro para archivos xeno-canto
            nuevo_registro.update({
                "vernacularName": "",
                "mediaType": "",
                "format": "",
                "license": ""
            })

    elif tipo_dataset == "inaturalist":
        #Registro para archivos inaturalist
        nuevo_registro = {
            "scientific_name": "",
            "latitude": 0.0,
            "longitude":0.0,
            "observed_on": "",
            "species_guess": "",
            "place_guess": "",
            "user_login": "",
            "quality_grade": "",
            "license": "",
            "image_url": ""      
        }

    else:
        raise ValueError ("Tipo de dataset no reconocido")
    
    return nuevo_registro


#===================== Punto 4B =======================
def inicializar_registro (lista_columnas):
    """
        Genera un registro vacio con una lista de columnas

        lista_columnas obtenemos los nombres de las columnas

        Devuelve el registro con cadena vacia
    """
    nuevo_registro = {}

    for columna in lista_columnas:
        nuevo_registro[columna] = ""
    
    return nuevo_registro


#===================== Punto 4C =======================
from validacion_registro import (validar_latitud_registro, validar_longitud_registro, validar_fecha_registro, validar_countryCode_registro, validar_incertidumbre_registro)

def agrupar_validaciones(registro):
    """
        Funcion 4C:

        Valida un registro antes insertarlo reutilizando y agrupando las funciones
        realizadas por mis compañeros anteriormente

        errores va a tener los errores encontrados. Estara vacio si no hay errores
    """
    errores = []

    #Verifica la latitud dependiendo si el registro tiene decimalLatitude o latitude
    if "decimalLatitude" in registro:
        errores.extend(validar_latitud_registro(registro["decimalLatitude"]))
    elif "latitude" in registro:
        errores.extend(validar_latitud_registro(registro["latitude"]))

    #Verifica la longitud dependiendo si el registro tiene decimalLongitude o longitude
    if "decimalLongitude" in registro:
        errores.extend(validar_longitud_registro(registro["decimalLongitude"]))
    elif "longitude" in registro:
        errores.extend(validar_longitud_registro(registro["longitude"]))

    #Verifica la fecha dependiendo si el registro tiene eventDate o observed_on
    if "eventDate" in registro:
        errores.extend(validar_fecha_registro(registro["eventDate"]))
    elif "observed_on" in registro:
        errores.extend(validar_fecha_registro(registro["observed_on"]))
    
    #Verifica el pais con CountryCode
    if "countryCode" in registro:
        errores.extend(validar_countryCode_registro(registro["countryCode"]))

    #Verifica la incertidumbre
    if "coordinateUncertaintyInMeters" in registro:
        errores.extend(validar_incertidumbre_registro(registro["coordinateUncertaintyInMeters"]))

    return len(errores) == 0, errores


#===================== Punto 4D =======================
import random

#se van a hacer tres casos distintos (iadiza, xeno-canto, inaturalist)
id_asignado_iadiza = 0

def preparar_para_csv(registro, tipo_dataset):
    """
        Prepara un registro para añadir al csv y le agrega un tipo de ID dependiendo
        del tipo de dataset

        Genera una copia del registro

        Los ID pueden ser:
            - iadiza: autoincremental
            - xenocanto: "XC" + numero random entre 1000 y 9999
            - inatualist: numero random entre 100000000  99999999

        Retorna la copia del registro con el ID añadido

        Nota: El ID de iadiza es global, entonces puede resetearse si el modulo
        se reimporta.
    """
    global id_asignado_iadiza
    nuevo_registro = registro.copy()

    if tipo_dataset == "iadiza":
        #autoincremental para archivo iadiza
        id_asignado_iadiza += 1
        nuevo_registro["id"] = id_asignado_iadiza

    elif tipo_dataset == "xenocanto":
        #prefijo XC + numero random para archivo xeno-canto
        nuevo_registro["id"] = "XC" + str(random.randint(1000, 9999))

    elif tipo_dataset == "inaturalist":
        #ID random para archivo inaturalist
        nuevo_registro["id"] = random.randint(100000000 , 999999999)

    return nuevo_registro


#===================== Punto 4F =======================
# Lectura y manejo de archivos
import csv
import os
from cargardataset import cargar_dataset

def agregar_registro(numero_dataset, tipo_dataset, carpeta_destino="processed_datasets"):
    """
        Lee un dataset original. Luego solicita un nuevo registro por teclado, lo valida con las funciones que se hicieron 
        anteriormente y lo agrega al archivo destino en processed_datasets

        origen_dataset: Ruta original del archivo dataset
        tipo_dataset: Tipo de dataset (iadiza, xenocanto, inaturalist)
        carpeta_destino: Carpeta donde se guarda el nuevo registro, en ese caso por defecto processed_datasets
    """
    #Cargamos el dataset de la misma manera que el punto 2
    dataset = cargar_dataset(numero_dataset)
    origen_dataset = dataset["ruta"]
    separador = dataset["separador"]

    #Crea la carpeta destino si no existe
    os.makedirs(carpeta_destino, exist_ok=True)
    #Hacemos la ruta del archivo
    archivo_destino = os.path.join(carpeta_destino, os.path.basename(str(origen_dataset)))

    #Lee los encabezados del dataset original
    with open(origen_dataset, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=separador)
        #leemos la primera fila para encabezados
        encabezados = next(reader)

    #inicializar registro vacío según el dataset (4.A)
    registro = inicio_registro(tipo_dataset)

    #pedimos datos por teclado para cada columna
    for col in registro.keys():
        valor = input(f"Ingrese valor para {col}: ")
        registro[col] = valor

    #validamos el registro antes de insertarlo (4C)
    errores = agrupar_validaciones(registro)
    #si la lista no esta vacia, hay errores
    if errores:
        print("El registro tiene errores y no puede ser insertado")
        for error in errores:
            #imprime cada error encontrada
            print(" -", error)
        #sale de la funcion sin insertar nada
        return

    #asignamos ID automáticamente (4.D)
    registro = preparar_para_csv(registro, tipo_dataset)
    if "id" not in encabezados:
        encabezados.append("id")

    #escribir en archivo destino
    existe = os.path.exists(archivo_destino)
    #cree un CSV que trabaja con diccionarios
    with open(archivo_destino, "a", encoding="utf-8", newline="") as f:
        #usa la lista de columnas de encabezados que leimos antes
        writer = csv.DictWriter(f, fieldnames=encabezados, delimiter=separador, extrasaction="ignore")
        if not existe:
            #si no existia la fila de encabezados lo escribe. Si ya existia no lo hace
            writer.writeheader()
        #escribe el nuevo diccionario que escribimos por teclado
        writer.writerow(registro)

    print("Registro agregado correctamente en", archivo_destino)


#===================== Punto 4G =======================
def agregar_multiples_registros(numero_dataset, tipo_dataset, cantidad, carpeta_destino="processed_datasets"):
    """
        Lee un dataset original, pide multiples registros por teclado, los valida y los agrega al archivo
        destino "processed_datasets"

        origen_dataset: Ruta del archivo original
        tipo_dataset: Tipo de dataset (iadiza, xenocanto, inaturalist)
        cantidad: Cantidad de registros que vamos a insertar
        carpeta_destino: Carpeta donde se guarda el nuevo archivo
    """
    for i in range(cantidad):
        print(f"\n-- Registro {i + 1} de {cantidad} --")
        agregar_registro(numero_dataset, tipo_dataset, carpeta_destino)