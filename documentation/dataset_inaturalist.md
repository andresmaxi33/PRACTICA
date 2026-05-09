# Dataset A3 - iNaturalist Filtered

## 1.A Información general

* **Nombre del dataset:** iNaturalist Filtered
* **Institución proveedora:** iNaturalist / GBIF
* **Cantidad de registros:** 1.229.610 registros
* **Cobertura geográfica:** Mundial
* **Cobertura temporal:** Actualización continua
* **Separador de campos utilizado:** Coma (`,`)
* **Codificación de caracteres (encoding):** UTF-8
* **Tipo de licencia:** Creative Commons BY-NC 4.0 (según archivo)
* **Frecuencia de actualización:** Muy frecuente / continua
* **Formato general:** CSV + metadatos XML

## Archivos del dataset y propósito

* **observations.csv** → archivo principal con observaciones de biodiversidad.
* **media.csv** → archivos multimedia asociados (imágenes, sonidos, etc.).
* **dna_derived_data.csv** → información derivada genética / ADN.
* **meta.xml** → estructura técnica del dataset.
* **eml.xml** → metadatos generales y licencia.

## 1.B Descripción de atributos del dataset

A continuación se describen atributos relevantes del archivo `observations.csv`.

* **id**
  Identificador único de la observación.
  **Ejemplo:** `987654321`

* **observed_on**
  Fecha en que se realizó la observación.
  **Ejemplo:** `2024-03-18`

* **scientific_name**
  Nombre científico de la especie observada.
  **Ejemplo:** `Passer domesticus`

* **species_guess**
  Nombre sugerido o estimado por el usuario.
  **Ejemplo:** `Gorrión común`

* **latitude**
  Latitud del lugar observado.
  **Ejemplo:** `-34.9205`

* **longitude**
  Longitud del lugar observado.
  **Ejemplo:** `-57.9536`

* **place_guess**
  Descripción textual del lugar.
  **Ejemplo:** `La Plata, Buenos Aires`

* **user_login**
  Usuario que cargó la observación.
  **Ejemplo:** `naturalista_2024`

* **quality_grade**
  Nivel de calidad asignado al registro.
  **Ejemplo:** `research`

* **license**
  Licencia de uso del contenido.
  **Ejemplo:** `CC BY-NC`

* **image_url**
  URL o referencia de imagen asociada.
  **Ejemplo:** `https://.../photo.jpg`
