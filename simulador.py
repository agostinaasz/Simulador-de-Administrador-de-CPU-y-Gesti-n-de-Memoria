procesos = []
memoria = []

reloj = 0
cant_terminados = 0
cpu_libre = True
en_ejecucion = None
hubo_llegada = False


def cargar_procesos(nombre_archivo):
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
                print("ERROR: el archivo contiene mas de 10 procesos")
                archivo.close()
                return None

    archivo.close()

    if len(procesos_cargados) == 0:
        print("ERROR: el archivo no contiene procesos")
        return None

    return procesos_cargados


def buscarBestFit(tam_buscado):
    pos_hueco = -1
    menor_tamaño = 451

    for j in range(len(memoria)):
        if memoria[j]["ocupado"] == 0 and memoria[j]["tamaño"] >= tam_buscado:
            if memoria[j]["tamaño"] < menor_tamaño:
                menor_tamaño = memoria[j]["tamaño"]
                pos_hueco = j

    return pos_hueco


def asignar_particion(i, pos_hueco):
    inicio_original = memoria[pos_hueco]["inicio"]
    tamaño_original = memoria[pos_hueco]["tamaño"]

    if tamaño_original == procesos[i]["tamaño"]:
        memoria[pos_hueco]["id_proceso"] = procesos[i]["id_proceso"]
        memoria[pos_hueco]["ocupado"] = 1

    else:
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
    i = 0

    while i < len(memoria) - 1:
        if memoria[i]["ocupado"] == 0 and memoria[i + 1]["ocupado"] == 0:
            memoria[i]["tamaño"] = memoria[i]["tamaño"] + memoria[i + 1]["tamaño"]
            memoria.pop(i + 1)
        else:
            i = i + 1

    for j in range(len(memoria)):
        memoria[j]["id_particion"] = j + 1


def mostrarEstado():
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

    input("Presione Enter para continuar")


def informeFinal():
    suma_retorno = 0
    suma_espera = 0

    print()
    print("Informe final")

    for proceso in procesos:
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

        if posmen != -1:
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
