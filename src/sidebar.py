import streamlit as st
from datetime import datetime
from cargar_dataset_DataFrames import DATASETS_CONFIG, _buscar_archivo, cargar_dataset_df

def listar_datasets_disponibles():
    """
    Retorna los nombres de los datasets que tienen archivo físico disponible.
    """
    disponibles = []
    for nombre in DATASETS_CONFIG:
        try:
            _buscar_archivo(nombre)
            disponibles.append(nombre)
        except FileNotFoundError:
            pass
    return disponibles


def render_sidebar():
    """
    Ejercicios 1B y 1C

    Muestra en el sidebar de Streamlit el selector de dataset (1B) 
    y el indicador de estado (1C).

    La elección del dataset se guarda en st.session_state 
    para mantenerse entre páginas.

    Debe llamarse al inicio de cada página que necesite trabajar con un dataset.
    """
    with st.sidebar:
        st.divider()
        st.subheader("📂 Dataset activo")

        # ── Ejercicio 1B: selector de dataset ───────────────────────────────
        datasets_disponibles = listar_datasets_disponibles()

        if not datasets_disponibles:
            st.warning("No hay datasets disponibles.")
            st.session_state["dataset_nombre"] = None
            st.session_state["dataset_df"] = None
            return

        # Determinar índice actual para no resetear la selección entre páginas
        indice_actual = 0
        if "dataset_nombre" in st.session_state and st.session_state["dataset_nombre"] in datasets_disponibles:
            indice_actual = datasets_disponibles.index(st.session_state["dataset_nombre"])

        seleccion = st.selectbox(
            "Seleccioná el dataset:",
            options=datasets_disponibles,
            index=indice_actual,
            key="selector_dataset_sidebar",
        )

        # Si cambió la selección o es la primera carga, recargamos el DataFrame
        if  seleccion != st.session_state.get("dataset_nombre") or "dataset_df" not in st.session_state or st.session_state["dataset_df"] is None:
            with st.spinner(f"Cargando {seleccion}..."):
                try:
                    df = cargar_dataset_df(seleccion)
                    st.session_state["dataset_nombre"] = seleccion
                    st.session_state["dataset_df"] = df
                    st.session_state["dataset_carga_hora"] = datetime.now()
                    if seleccion != st.session_state.get("dataset_nombre"):
                        st.toast("Dataset cargado ✓", icon="✅")
                except Exception as e:
                    st.error(f"Error al cargar: {e}")
                    st.session_state["dataset_df"] = None
                    return
                
        # ── Ejercicio 1C: indicador del dataset activo ───────────────────────
        df_activo = st.session_state.get("dataset_df")
        nombre_activo = st.session_state.get("dataset_nombre", "—")
        hora_carga = st.session_state.get("dataset_carga_hora")

        if df_activo is not None:
            st.markdown("**📊 Dataset activo:**")
            st.markdown(f"- **Nombre:** {nombre_activo}")
            st.markdown(f"- **Registros:** {len(df_activo):,}")
            if hora_carga:
                st.markdown(f"- **Cargado:** {hora_carga.strftime('%d/%m/%Y %H:%M:%S')}")
        else:
            st.info("Ningún dataset cargado.")