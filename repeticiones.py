from datetime import datetime
from datetime import date
from datetime import timedelta

import json
import math

fileObject1 = open("modulos.json", "r")
jsonContent = fileObject1.read()
modulos = json.loads(jsonContent)

name_arr = []
for each in modulos:
    name_arr.append(each['name'])

#tengo los nombres del qhawax en name_arr para que de una sola corrida
#me obtenga los datos repetidos de todos los JSON
k = 0
while(k < int(len(name_arr))):
    name_file = name_arr[k] + "_processed.json"
    fileObject =  open(name_file, "r")
    jsonContent = fileObject.read()

    #aqui tengo mi lista con los dicts
    data = json.loads(jsonContent)

    #Cambio el formato de string a datetime
    for each in data:
        each['timestamp_zone']=datetime.strptime(each['timestamp_zone'], '%a, %d %b %Y %H:%M:%S GMT')

    #sensor_array: aquellos datos que se analizaran
    sensor_array = ['humidity','pressure','temperature',
                'SPL','I_temperature','UV','CO_ug_m3',
                'H2S_ug_m3','NO2_ug_m3','O3_ug_m3',
                'PM1','PM10','PM25','SO_ug_m3']

    # variable que servira de tope para el contador
    n_sensors = int(len(sensor_array))

    # dict que contendra aquellas medidas repetidas
    repetidos = {}
    qhawax_arr = []

    # tope del contador "i", es la cantidad de dicts dentro de la lista data.
    n = int(len(data))

    minutos = 5
    segundos_max = minutos*60
    j = 0
    while j<n_sensors:
        # iterando en cada dato correspondiente a un mismo sensor de la lista
        # de interes
        i = 1
        #acc: contador que se acumulara en segundos cuando encuentra repetidos
        #     para compararlo con 300 segundos
        acc = 0
        while i<n:
            # se verifica que el sensor exista en la data para evitar errores
            if((sensor_array[j]) in data[i-1])and((sensor_array[j]) in data[i]):
                # si se repite un dato de las medidas
                x1 = data[i][sensor_array[j]]
                x0 = data[i-1][sensor_array[j]]
                if (x1 == x0):
                        acc += ((data[i]['timestamp_zone'])-(data[i-1]['timestamp_zone'])).total_seconds()
                        # si acc supera los "segundos_max" segundos con la misma medida
                        if acc >= segundos_max:
                            repetidos[str(sensor_array[j])] = str(x1)
                else:
                # si no hay repeticion con el anterior, el contador de segundos es reseteado
                    acc = 0
                i += 1
            else:
                i += 1
        j += 1
    if repetidos!={}:
        print(" ")
        print(name_arr[k] + " envio el mismo valor en un periodo de 5 min")
        print(" ")
        json_rep = json.dumps(repetidos)
        print("Se congelaron los siguientes valores: " + (json_rep))
        print(" ")
    k += 1
