# 📊 Trabajo Integrador 2026

## Taller de Lenguajes -- Python -- Grupo 46

------------------------------------------------------------------------

## 👥 Integrantes

-   Andrés Maximiliano Sales\
-   Agustin Bruno\
-   Juan Pablo Tolaba\
-   Natalia Belén López

------------------------------------------------------------------------

## 🧩 Descripción

Proyecto de **análisis y visualización de datos de biodiversidad** bajo
el estándar **Darwin Core**.

La aplicación permite: - 🧹 Sanitización de datos\
- ✅ Validación de registros biológicos\
- 🔍 Consulta eficiente de información\
- 📈 Visualización interactiva mediante **Streamlit**

------------------------------------------------------------------------

## 📁 Estructura del Repositorio

    📦 proyecto/
     ┣ 📂 documentation/         # Documentación técnica en Markdown
     ┣ 📂 raw_datasets/          # Datos originales (vacía en remoto)
     ┣ 📂 processed_datasets/    # Datos procesados (vacía en remoto)
     ┣ 📂 src/                   # Código fuente modular en Python
     ┣ 📂 notebooks/             # Notebooks de prueba (Jupyter)
 

------------------------------------------------------------------------

## ⚙️ Guía de Configuración y Ejecución

### 1️⃣ Crear entorno virtual

#### 🪟 Windows (Git Bash / PowerShell)

``` bash
python -m venv venv
source venv/Scripts/activate
# En PowerShell:
.\venv\Scripts\Activate.ps1
```

#### 🐧 Linux / 🍎 Mac

``` bash
python3 -m venv venv
source venv/bin/activate
```

------------------------------------------------------------------------

### 2️⃣ Instalar dependencias

``` bash
pip install -r requirements.txt
```

📌 Si aún no existe:

``` bash
pip freeze > requirements.txt
```

------------------------------------------------------------------------

### 3️⃣ Ejecutar el proyecto

#### 📓 Notebooks (Jupyter)

``` bash
jupyter notebook
```

Luego abrir:

    notebooks/ejercicio6a.ipynb

------------------------------------------------------------------------

#### 🌐 Aplicación web (Streamlit)

``` bash
streamlit run main.py
```

------------------------------------------------------------------------

## ⚠️ Consideraciones de la Cátedra

-   ❌ No subir archivos a:
    -   `raw_datasets/`
    -   `processed_datasets/`
-   ✔️ Mantener el repositorio limpio y liviano

