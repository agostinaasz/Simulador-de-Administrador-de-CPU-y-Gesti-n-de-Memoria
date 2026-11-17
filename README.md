# Simulador de Memoria y Planificación de Procesos

Trabajo Práctico Integrador de la materia Sistemas Operativos.

El proyecto consiste en un simulador desarrollado en Python para representar el funcionamiento de la gestión de memoria y la planificación de procesos.

## Características principales

El simulador implementa:

- Gestión de memoria mediante particiones variables.
- Asignación de memoria utilizando el algoritmo Best-Fit.
- Planificación de CPU mediante SRTF.
- Manejo de los estados Nuevo, Listo, Listo/Suspendido, Ejecución y Terminado.
- Un máximo de cinco procesos admitidos simultáneamente.
- Un máximo de diez procesos por lote.
- 100K de memoria reservados para el Sistema Operativo y 450K disponibles para los procesos.
- Liberación de memoria al finalizar un proceso.
- Unificación de huecos libres contiguos.
- Visualización del estado actual de la CPU, los procesos y las particiones de memoria.
- Cálculo del tiempo de retorno y del tiempo de espera de cada proceso.
- Cálculo de los promedios de retorno y espera.
- Cálculo del rendimiento general del sistema.

## Ejecución

El simulador se ejecuta desde el archivo `simulador.py`.

Los lotes de procesos utilizados para las pruebas se encuentran dentro de la carpeta `lotes`.

Al comenzar la ejecución, el programa solicita el archivo correspondiente al lote de procesos. A partir de ese momento, la simulación avanza mostrando los cambios producidos en el sistema hasta que todos los procesos finalizan.

Durante la ejecución se presentan:

- El valor actual del reloj.
- El estado de la CPU.
- Los procesos que ya ingresaron al sistema.
- El estado actual de cada proceso.
- La distribución de las particiones de memoria.
- El proceso asignado a cada partición.
- El tiempo restante de ejecución de los procesos.

Al finalizar, se muestra un informe con las métricas obtenidas durante la simulación.
