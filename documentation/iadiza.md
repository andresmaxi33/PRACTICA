# Dataset - Colección Ornitológica del IADIZA - CCT CONICET Mendoza

## 1.A Información general

* **Nombre del dataset:** Colección Ornitológica del IADIZA - CCT CONICET Mendoza (IADIZA-COI)
* **Institución proveedora:** IADIZA / CONICET / publicado vía GBIF
* **Cantidad de registros:** 2.370 registros
* **Cobertura geográfica:** Principalmente Mendoza, Argentina
* **Cobertura temporal:** Registros históricos de colección biológica
* **Separador de campos utilizado:** Tabulación (`\t`)
* **Codificación de caracteres (encoding):** UTF-8
* **Tipo de licencia:** Según condiciones de GBIF y dataset fuente
* **Frecuencia de actualización:** No periódica fija / según nuevas publicaciones o cargas
* **Formato general:** Darwin Core Archive

## Archivos del dataset y propósito

* **occurrence.txt** → archivo principal con registros biológicos y taxonómicos.
* **verbatim.txt** → datos originales tal como fueron cargados por la fuente.
* **metadata.xml** → metadatos generales del dataset.
* **meta.xml** → estructura técnica de archivos, columnas y relaciones.
* **citations.txt** → citas bibliográficas del dataset.
* **multimedia.txt** → referencias a imágenes u otros recursos multimedia.
* **rights.txt** → información de derechos y uso.

## 1.B Descripción de atributos del dataset

A continuación se describen algunos atributos relevantes del archivo principal `occurrence.txt`.

* **gbifID**
  Identificador único global del registro dentro de GBIF.
  **Ejemplo:** `3456789012`

* **occurrenceID**
  Código único del registro en la colección original.
  **Ejemplo:** `IADIZA-AV-00215`

* **basisOfRecord**
  Tipo de registro biológico.
  **Ejemplo:** `PreservedSpecimen`

* **scientificName**
  Nombre científico completo de la especie.
  **Ejemplo:** `Zenaida auriculata`

* **kingdom**
  Reino biológico.
  **Ejemplo:** `Animalia`

* **phylum**
  Filo taxonómico.
  **Ejemplo:** `Chordata`

* **class**
  Clase taxonómica.
  **Ejemplo:** `Aves`

* **order**
  Orden taxonómico.
  **Ejemplo:** `Columbiformes`

* **family**
  Familia taxonómica.
  **Ejemplo:** `Columbidae`

* **genus**
  Género biológico.
  **Ejemplo:** `Zenaida`

* **decimalLatitude**
  Latitud geográfica del registro.
  **Ejemplo:** `-32.8895`

* **decimalLongitude**
  Longitud geográfica del registro.
  **Ejemplo:** `-68.8458`

* **country**
  País donde se registró el ejemplar.
  **Ejemplo:** `Argentina`

* **stateProvince**
  Provincia o región administrativa.
  **Ejemplo:** `Mendoza`

* **eventDate**
  Fecha de colecta u observación.
  **Ejemplo:** `1998-11-15`

* **recordedBy**
  Persona responsable del registro.
  **Ejemplo:** `Juan Pérez`
