"""
============================================================================================
TRABAJO PRÁCTICO INTEGRADOR: SIMULADOR DE ASIGNACIÓN DE MEMORIA Y PLANIFICACION DE PROCESOS
Integrantes: 
    Almirón Bechert, Gabriel Alejo.
    Bogado, Sharon Tatiana.
    Gesto, Emiliano Joaquin.
    Korovaichuk, Dilan Lautaro.
    Navarro, Maiha Antonella.
    Segovia, Agostina Victoria Jacqueline.
============================================================================================
Estados de los procesos: 
    0: Nuevo 
    1: Listo
    2: Listo y suspendido
    3: Ejecucion
    4: Terminado
"""
# estructuras principales de la simulacion.
procesos = [] # para guardar la info de cada proceso
memoria = [] # para las particiones 

# variables generales para controlar el avance y el estado de la simulacion
reloj = 0
cant_terminados = 0
cpu_libre = True
en_ejecucion = None
hubo_llegada = False


def cargar_procesos(nombre_archivo):
    """
    lee los procesos desde el archivo de entrada y valida su formato.
    Cada linea contiene: proceso, tiempo de arribo, tiempo de irrupcion y tamaño.
    Retorna la lista cargada o None si encuentra un error.
    """
    procesos_cargados = []

    try:
        archivo = open(nombre_archivo, "r", encoding="utf-8")
    except FileNotFoundError:
        print("ERROR: no se encontro el archivo")
        return None

    for linea in archivo:
        linea = linea.strip()

        if linea != "":
            datos = linea.split()

            if len(datos) != 4:
                print("ERROR: formato incorrecto en el archivo")
                archivo.close()
                return None

            try:
                id_proceso = datos[0]
                tiempo_arribo = int(datos[1])
                tiempo_irrupcion = int(datos[2])
                tamaño = int(datos[3])
            except ValueError:
                print("ERROR: los datos del proceso son incorrectos")
                archivo.close()
                return None

            if tamaño > 450:
                print("ERROR: el proceso", id_proceso, "supera los 450K disponibles")
                archivo.close()
                return None

            proceso = {
                "id_proceso": id_proceso,
                "tamaño": tamaño,
                "tiempo_arribo": tiempo_arribo,
                "tiempo_irrupcion": tiempo_irrupcion,
                "tiempo_restante": tiempo_irrupcion,
                "estado": 0,
                "tiempo_finalizacion": 0
            }

            procesos_cargados.append(proceso)

            if len(procesos_cargados) > 10:
                # la consigna permite solo un maximo de 10 procesos.
                print("ERROR: el archivo contiene mas de 10 procesos")
                archivo.close()
                return None

    archivo.close()

    if len(procesos_cargados) == 0:
        print("ERROR: el archivo no contiene procesos")
        return None

    return procesos_cargados


def buscarBestFit(tam_buscado):
    """
    busca mediante el algoritmo best fit el hueco libre mas pequeño donde pueda entrar
    un proceso del tamaño indicado. Retorna su posicion o -1 si no existe.
    """
    pos_hueco = -1
    # 451 se usa porque el mayor hueco posible de memoria para procesos es de 450k
    menor_tamaño = 451

    for j in range(len(memoria)):
        if memoria[j]["ocupado"] == 0 and memoria[j]["tamaño"] >= tam_buscado:
            if memoria[j]["tamaño"] < menor_tamaño:
                menor_tamaño = memoria[j]["tamaño"]
                pos_hueco = j

    return pos_hueco


def asignar_particion(i, pos_hueco):
    """
    asigna al proceso la particion encontrada por best fit.
    Si sobra espacio, divide el hueco y mantiene el resto como memoria libre.
    El proceso pasa al estado Listo.
    """
    inicio_original = memoria[pos_hueco]["inicio"]
    tamaño_original = memoria[pos_hueco]["tamaño"]

    if tamaño_original == procesos[i]["tamaño"]:
        memoria[pos_hueco]["id_proceso"] = procesos[i]["id_proceso"]
        memoria[pos_hueco]["ocupado"] = 1

    else:
         # si el hueco es mayor que el proceso el sobrante queda como una nueva particion libre
        memoria[pos_hueco]["inicio"] = inicio_original
        memoria[pos_hueco]["tamaño"] = procesos[i]["tamaño"]
        memoria[pos_hueco]["id_proceso"] = procesos[i]["id_proceso"]
        memoria[pos_hueco]["ocupado"] = 1

        nueva_particion = {
            "id_particion": 0,
            "inicio": inicio_original + procesos[i]["tamaño"],
            "tamaño": tamaño_original - procesos[i]["tamaño"],
            "id_proceso": None,
            "ocupado": 0
        }

        memoria.insert(pos_hueco + 1, nueva_particion)

    for j in range(len(memoria)):
        memoria[j]["id_particion"] = j + 1

    procesos[i]["estado"] = 1


def unificarHuecos():
    """
    recorre las particiones y fusiona los huecos libres contiguos para evitar la fragmentacion externa 
    formando bloques libres mas grandes.
    """
    i = 0

    while i < len(memoria) - 1:
        if memoria[i]["ocupado"] == 0 and memoria[i + 1]["ocupado"] == 0:
            memoria[i]["tamaño"] = memoria[i]["tamaño"] + memoria[i + 1]["tamaño"]
            memoria.pop(i + 1) 
            #aca no incremento i porque la nueva part que cayo en i+1 tmb podria estar libre y necesitar fusionarse con i (te estarias salteando una)
        else:
            i = i + 1

    for j in range(len(memoria)):
        memoria[j]["id_particion"] = j + 1


def mostrarEstado():
    """
    muestra el estado actual de la cpu, las particiones de memoria,
    la cola de Listos y la cola de listos y suspendidos.
    """
    print()
    print("Reloj:", reloj)

    if cpu_libre:
        print("CPU libre")
    else:
        print("Proceso en ejecucion:", procesos[en_ejecucion]["id_proceso"])

    print("Particiones de memoria")

    for particion in memoria:
        if particion["ocupado"] == 1:
            print(
                "Particion", particion["id_particion"],
                "Inicio:", particion["inicio"],
                "Tamaño:", particion["tamaño"],
                "Proceso:", particion["id_proceso"],
                "Fragmentacion interna: 0"
            )
        else:
            print(
                "Particion", particion["id_particion"],
                "Inicio:", particion["inicio"],
                "Tamaño:", particion["tamaño"],
                "Libre",
                "Fragmentacion interna: 0"
            )

    print("Procesos listos")

    hay_listos = False

    for proceso in procesos:
        if proceso["estado"] == 1:
            print(
                "Proceso", proceso["id_proceso"],
                "Tiempo restante:", proceso["tiempo_restante"]
            )
            hay_listos = True

    if hay_listos == False:
        print("No hay procesos listos")

    print("Procesos listos y suspendidos")

    hay_suspendidos = False

    for proceso in procesos:
        if proceso["estado"] == 2:
            print(
                "Proceso", proceso["id_proceso"],
                "Tiempo restante:", proceso["tiempo_restante"]
            )
            hay_suspendidos = True

    if hay_suspendidos == False:
        print("No hay procesos listos y suspendidos")

    input("Presione ENTER para continuar")


def informeFinal():
    """
    calcula y muestra el tiempo de retorno y espera de cada proceso,
    sus promedios y el rendimiento final del sistema.
    """
    suma_retorno = 0
    suma_espera = 0

    print()
    print("Informe final")

    for proceso in procesos:
         # calculo de las metricas pedidas para cada proceso
        tiempo_retorno = proceso["tiempo_finalizacion"] - proceso["tiempo_arribo"]
        tiempo_espera = tiempo_retorno - proceso["tiempo_irrupcion"]

        print()
        print("Proceso", proceso["id_proceso"])
        print("Tiempo de retorno:", tiempo_retorno)
        print("Tiempo de espera:", tiempo_espera)

        suma_retorno = suma_retorno + tiempo_retorno
        suma_espera = suma_espera + tiempo_espera

    prom_retorno = suma_retorno / len(procesos)
    prom_espera = suma_espera / len(procesos)

    if reloj > 0:
        rendimiento = cant_terminados / reloj
    else:
        rendimiento = 0

    print()
    print("Promedio de tiempo de retorno:", prom_retorno)
    print("Promedio de tiempo de espera:", prom_espera)
    print("Rendimiento del sistema:", rendimiento)


def tratar_ejecucion(posmen):
    """
    simula la ejecucion con una unidad de reloj para el proceso seleccionado.
    descuenta el tiempo restante de irrupcion y si finaliza marca al proceso como terminado, libera la memoria 
    que ocupaba y ejecuta la unificacion de huecos mostrando el estado.
    """
    global reloj
    global cant_terminados
    global cpu_libre
    global en_ejecucion
    global hubo_llegada

    cpu_libre = False
    procesos[posmen]["estado"] = 3
    en_ejecucion = posmen

    if hubo_llegada:
        mostrarEstado()
        hubo_llegada = False

    reloj = reloj + 1
    procesos[posmen]["tiempo_restante"] = procesos[posmen]["tiempo_restante"] - 1

    if procesos[posmen]["tiempo_restante"] == 0:
        procesos[posmen]["estado"] = 4
        procesos[posmen]["tiempo_finalizacion"] = reloj
        cant_terminados = cant_terminados + 1

        for particion in memoria:
            if particion["id_proceso"] == procesos[posmen]["id_proceso"]:
                particion["id_proceso"] = None
                particion["ocupado"] = 0

        cpu_libre = True
        en_ejecucion = None

        unificarHuecos()
        mostrarEstado()


def planificacionCPU():
    """
    agarra el proceso con el menor tiempo restante de la cola de listos.
    si la cpu esta ocupada y llega un proceso con menor t restante que el actual, expropia
    la cpu mandando el proceso actual de vuelta a Listo.
    """
    global reloj
    global hubo_llegada

    if cpu_libre:
        posmen = -1

        for i in range(len(procesos)):
            if procesos[i]["estado"] == 1:
                if posmen == -1:
                    posmen = i
                else:
                    if procesos[i]["tiempo_restante"] < procesos[posmen]["tiempo_restante"]:
                        posmen = i

        if posmen != -1: #esto por si no habia ninguno listo y la cpu esta ociosa y no intentar acceder a la pos -1 que va a dar error.
            tratar_ejecucion(posmen)

        else:
            if hubo_llegada:
                mostrarEstado()
                hubo_llegada = False

            reloj = reloj + 1

    else:
        posmen = en_ejecucion

        for i in range(len(procesos)):
            if procesos[i]["estado"] == 1:
                # srtf solo expropia si aparece un proceso con menor tiempo restante
                if procesos[i]["tiempo_restante"] < procesos[posmen]["tiempo_restante"]:
                    posmen = i

        if posmen != en_ejecucion:
            procesos[en_ejecucion]["estado"] = 1

        tratar_ejecucion(posmen)


nombre_archivo = input("Ingrese el nombre del archivo de procesos: ")

procesos_leidos = cargar_procesos(nombre_archivo)

if procesos_leidos is not None:
    procesos = procesos_leidos
    
    memoria = [
        # los primeros 100k le corresponden al sistema operativo
        # los 450k restantes quedan inicialmente libres para los procesos
        {
            "id_particion": 1,
            "inicio": 100,
            "tamaño": 450,
            "id_proceso": None,
            "ocupado": 0
        }
    ]

    reloj = 0
    cant_terminados = 0
    cpu_libre = True
    en_ejecucion = None

    while cant_terminados < len(procesos):
        hubo_llegada = False

        for i in range(len(procesos)):
            if procesos[i]["estado"] == 2:
                pos_hueco = buscarBestFit(procesos[i]["tamaño"])

                if pos_hueco != -1:
                    asignar_particion(i, pos_hueco)

                    print(
                        "Proceso",
                        procesos[i]["id_proceso"],
                        "pasa de LISTO Y SUSPENDIDO a LISTO"
                    )

        for i in range(len(procesos)):
            if procesos[i]["estado"] == 0 and procesos[i]["tiempo_arribo"] <= reloj:

                if procesos[i]["tiempo_arribo"] == reloj:
                    hubo_llegada = True

                cant_admitidos = 0

                for proceso in procesos:
                    if proceso["estado"] == 1 or proceso["estado"] == 2 or proceso["estado"] == 3:
                        cant_admitidos = cant_admitidos + 1
                # como maximo puede haber 5 procesos entre ejecucion, listos y listos/suspendidos
                if cant_admitidos < 5:
                    pos_hueco = buscarBestFit(procesos[i]["tamaño"])

                    if pos_hueco == -1:
                        procesos[i]["estado"] = 2

                        print(
                            "Proceso",
                            procesos[i]["id_proceso"],
                            "pasa a LISTO Y SUSPENDIDO"
                        )

                    else:
                        asignar_particion(i, pos_hueco)

                        print(
                            "Proceso",
                            procesos[i]["id_proceso"],
                            "pasa a LISTO"
                        )

        planificacionCPU()

    informeFinal()
