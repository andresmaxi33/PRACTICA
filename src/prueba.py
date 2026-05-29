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
# =====================================================

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

from cargardataset import cargar_dataset

st.set_page_config(page_title="Búsqueda", layout="wide")
st.title("🔍 Búsqueda de Registros de Biodiversidad")

# ==================== CARGA ====================
if "dataset_numero" not in st.session_state or st.session_state.dataset_numero is None:
    st.warning(" Por favor selecciona un dataset en la página **Inicio**.")
    st.stop()  # Detiene la ejecución de la página
# CARGA
config = cargar_dataset(st.session_state.get("dataset_numero"))
df = pd.read_csv(
    config["ruta"],
    sep=config["separador"],
    encoding=config["encoding"],
    low_memory=False,
)

st.success(f"Dataset activo: **{config['nombre']}** - {len(df):,} registros")

# FILTROS
st.sidebar.header("🔎 Filtros de Búsqueda")

columna_busqueda = st.sidebar.selectbox("Buscar en columna:", df.columns.tolist())
texto_buscar = st.sidebar.text_input("Texto a buscar:")

scientific_selected = st.sidebar.multiselect(
    "Nombre Científico",
    options=sorted(df["scientificName"].dropna().unique())
    if "scientificName" in df.columns
    else [],
)

country_col = "country" if "country" in df.columns else "countryCode"
country_selected = st.sidebar.multiselect(
    "País",
    options=sorted(df[country_col].dropna().unique())
    if country_col in df.columns
    else [],
)

province_selected = st.sidebar.multiselect(
    "Provincia",
    options=sorted(df["stateProvince"].dropna().unique())
    if "stateProvince" in df.columns
    else [],
)

observador = st.sidebar.text_input("Observador (recordedBy):")

# APLICAR FILTROS SOLO SI HAY ALGO
filtered_df = df.copy()

if texto_buscar and texto_buscar.strip():
    filtered_df = filtered_df[
        filtered_df[columna_busqueda]
        .astype(str)
        .str.contains(texto_buscar.strip(), case=False, na=False)
    ]

if scientific_selected:
    filtered_df = filtered_df[filtered_df["scientificName"].isin(scientific_selected)]

if country_selected and country_col in filtered_df.columns:
    filtered_df = filtered_df[filtered_df[country_col].isin(country_selected)]

if province_selected and "stateProvince" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["stateProvince"].isin(province_selected)]

if observador and observador.strip() and "recordedBy" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["recordedBy"]
        .astype(str)
        .str.contains(observador.strip(), case=False, na=False)
    ]

# MOSTRAR
st.subheader(f"📋 Resultados: **{len(filtered_df)}** registros encontrados")

if len(filtered_df) == 0:
    st.error("❌ No se encontraron registros. Prueba quitando todos los filtros.")
else:
    st.success(f"✅ Mostrando {len(filtered_df)} registros")

cols = [
    "scientificName",
    "countryCode",
    "stateProvince",
    "eventDate",
    "recordedBy",
    "decimalLatitude",
    "decimalLongitude",
]
cols = [c for c in cols if c in filtered_df.columns]

st.dataframe(filtered_df[cols], use_container_width=True, hide_index=True)

# Exportar y Resumen (mismo de antes)
if st.button("📥 Exportar resultados como CSV") and not filtered_df.empty:
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar CSV", csv, f"busqueda_{config['nombre']}.csv", "text/csv"
    )

st.subheader("📊 Resumen")
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Especies",
    filtered_df["scientificName"].nunique()
    if "scientificName" in filtered_df.columns
    else 0,
)
c2.metric("Países", filtered_df.get(country_col, pd.Series()).nunique())
c3.metric("Provincias", filtered_df.get("stateProvince", pd.Series()).nunique())
c4.metric("Observadores", filtered_df.get("recordedBy", pd.Series()).nunique())
