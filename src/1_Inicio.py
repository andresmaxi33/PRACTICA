import streamlit as st

# ==========================================
# ARCHIVO PRINCIPAL DE LA APLICACION
# ==========================================
# Ejecutar con:
# streamlit run src/1_Inicio.py
# ==========================================

# Titulo de la aplicacion
st.title("Aplicacion de Analisis de Biodiversidad")

# Proposito de la aplicacion
st.header("Proposito de la aplicacion")
st.write("""
La aplicacion tiene como objetivo facilitar el analisis de datos de biodiversidad,
permitiendo la consulta y visualizacion de registros de especies animales y vegetales. 
Estos datos se encuentran estructurados de acuerdo al estandar Darwin Core y se procesan 
para detectar inconsistencias, validar coordenadas y mejorar la calidad de los datos.
""")

# Importancia del analisis de datos de biodiversidad
st.header("Importancia del analisis de datos de biodiversidad")
st.write("""
Los datos de biodiversidad son fundamentales para la investigacion cientifica, la conservacion
y la gestion de los ecosistemas. A traves del analisis de estos datos, se pueden identificar
patrones en la distribucion de especies, cambios en los ecosistemas y los efectos del cambio
climatico sobre la fauna y la flora.

El acceso y analisis de estos datos tambien apoya la toma de decisiones para politicas publicas
y la conservacion de especies en peligro de extincion.
""")

# Explicacion sobre Darwin Core
st.header("¿Que es Darwin Core?")
st.write("""
Darwin Core es un estandar internacional que se utiliza para representar y compartir datos
relacionados con la biodiversidad. Este estandar facilita el intercambio de informacion sobre
especies, ubicacion geografica, fechas de observacion y otros detalles biologicos entre 
instituciones cientificas a nivel global.

Algunos de los campos mas comunes incluyen:

- Nombre cientifico de la especie
- Ubicacion geografica (latitud, longitud)
- Fecha y hora de la observacion
- Institucion proveedora de los datos
""")

# Instrucciones basicas de uso de la aplicacion
st.header("Instrucciones basicas de uso")
st.write("""
- **Navegacion entre paginas:** Use el menu lateral izquierdo para navegar entre las distintas secciones de la aplicacion. 
  Las opciones incluyen:
    - **Inicio:** Informacion sobre la aplicacion y su proposito.
    - **Estado del sistema:** Visualizacion de los logs de operaciones realizados.
    - **Busqueda (en construccion):** Futura seccion para busqueda avanzada en los datos.
    - **Visualizacion (en construccion):** Futura seccion para generar visualizaciones interactivas.
    
- **Consulta de informacion:** En esta aplicacion podra consultar registros de especies, explorar el estado del sistema y validar datos de biodiversidad.
""")
