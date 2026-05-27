import os

import streamlit as st

# Que hace:
# - Muestra el contenido del archivo de logs 'operations.log'.
# - Visualiza las operaciones realizadas en formato tabular.
# - Incluye fecha, hora, dataset, operacion, cantidad y estado.


st.title("Estado del sistema")
st.write("Visualización del archivo de operaciones del sistema")

# Ruta absoluta al archivo log (sube dos niveles desde pages/ hasta la carpeta logs/)
ruta = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../logs/operations.log")
)

try:
    # Abrir el archivo en modo lectura con codificacion UTF-8
    archivo = open(ruta, encoding="utf-8")
    lineas = archivo.readlines()
    archivo.close()

    datos = []

    for linea in lineas:
        linea = linea.strip()

        # Ignorar líneas vacias
        if linea == "":
            continue

        partes = linea.split()

        # Verificar cantidad mínima de partes (fecha, hora, dataset, operacion, cantidad, estado)
        if len(partes) >= 6:
            fecha = partes[0]
            hora = partes[1]
            dataset = partes[2]
            operacion = partes[3]
            cantidad = partes[4] + " " + partes[5]

            estado = ""
            # Si existe estado adicional
            if len(partes) >= 7:
                estado = partes[6]

            datos.append(
                {
                    "Fecha": fecha,
                    "Hora": hora,
                    "Dataset": dataset,
                    "Operacion": operacion,
                    "Cantidad": cantidad,
                    "Estado": estado,
                }
            )

    if len(datos) > 0:
        st.table(datos)
    else:
        st.write("El archivo de logs no contiene datos válidos")

except FileNotFoundError:
    st.write("No existe el archivo operations.log")
