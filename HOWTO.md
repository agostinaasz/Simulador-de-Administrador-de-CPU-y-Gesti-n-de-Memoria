# HowTo - Simulador de Memoria y Planificación de Procesos

## Requisitos

Para ejecutar el código fuente se necesita:

- Python instalado en el equipo.
- Los archivos del proyecto descargados en una misma carpeta.

## Ejecución desde el código fuente

El archivo principal del simulador es:

`simulador.py`

Al ejecutarlo, el programa solicita la ruta del archivo que contiene el lote de procesos.

Los archivos de prueba se encuentran dentro de la carpeta `lotes`, por lo que se debe ingresar la ruta correspondiente al archivo que se quiera utilizar.

Durante la simulación, el programa muestra:

- El valor actual del reloj.
- El proceso que ocupa la CPU.
- Los procesos que ya ingresaron al sistema y su estado.
- La distribución actual de la memoria.
- Las particiones ocupadas y libres.
- El tiempo restante de ejecución de cada proceso.

La simulación se detiene en los puntos de presentación y continúa cuando el usuario presiona ENTER.

## Archivos de entrada

Cada proceso debe contener los siguientes datos:

- Identificador del proceso.
- Tiempo de arribo.
- Tiempo de irrupción.
- Tamaño requerido en memoria.

El simulador admite como máximo diez procesos por lote y cada proceso puede solicitar hasta 450K de memoria.

## Finalización

Cuando todos los procesos terminan, el simulador muestra un informe final con:

- Tiempo de retorno de cada proceso.
- Tiempo de espera de cada proceso.
- Promedio de tiempo de retorno.
- Promedio de tiempo de espera.
- Rendimiento general del sistema.

## Ejecutable

También se incluye una versión ejecutable del simulador para Windows.

El ejecutable puede iniciarse directamente sin necesidad de abrir el código fuente.
