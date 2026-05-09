# Dataset - Xeno-canto Bird Sounds Filtered

## 1.A Información general

* **Nombre del dataset:** Xeno-canto Bird Sounds Filtered
* **Institución proveedora:** Xeno-canto / GBIF
* **Cantidad de registros:** 13.471 registros
* **Cobertura geográfica:** Mundial
* **Cobertura temporal:** Variable según fecha de grabación/publicación
* **Separador de campos utilizado:** Tabulación (`\t`)
* **Codificación de caracteres (encoding):** UTF-8
* **Tipo de licencia:** Creative Commons BY-NC 4.0
* **Frecuencia de actualización:** Periódica / colaborativa
* **Formato general:** Darwin Core Archive

## Archivos del dataset y propósito

* **Occurrence.txt** → archivo principal con registros de observaciones y grabaciones.
* **Multimedia.txt** → enlaces y datos de archivos de audio.
* **meta.xml** → estructura del dataset y definición de columnas.
* **eml.xml** → metadatos descriptivos generales.

## 1.B Descripción de atributos del dataset

A continuación se describen atributos relevantes del archivo `Occurrence.txt`.

* **id**
  Identificador del registro.
  **Ejemplo:** `XC123456`

* **scientificName**
  Nombre científico del ave grabada.
  **Ejemplo:** `Turdus rufiventris`

* **vernacularName**
  Nombre común de la especie.
  **Ejemplo:** `Zorzal colorado`

* **basisOfRecord**
  Tipo de registro.
  **Ejemplo:** `HumanObservation`

* **eventDate**
  Fecha de la grabación.
  **Ejemplo:** `2021-10-03`

* **country**
  País donde se realizó la grabación.
  **Ejemplo:** `Argentina`

* **decimalLatitude**
  Latitud geográfica.
  **Ejemplo:** `-34.9214`

* **decimalLongitude**
  Longitud geográfica.
  **Ejemplo:** `-57.9544`

* **recordedBy**
  Persona que realizó la grabación.
  **Ejemplo:** `Carlos Gómez`

* **mediaType**
  Tipo de recurso multimedia.
  **Ejemplo:** `Sound`

* **format**
  Formato del archivo multimedia.
  **Ejemplo:** `audio/mpeg`

* **license**
  Licencia de uso del recurso.
  **Ejemplo:** `CC BY-NC 4.0`
