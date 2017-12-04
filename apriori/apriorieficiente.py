# -*- coding: utf-8 -*-
import sys
import os
from itertools import chain, combinations

'''
     ____________________________________________________________________
    |                   CONVENCIONES DE NOMENCLATURA                     |
    |▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔|
    | - Si tenemos doble letra significa mayuscula. Ejemplo: ff == F.    |
    | - Si tenemos x implica subindice. Ejemplo ffx == Fx (subinidice x).|
    | - Comentarios con triple apostrofe (multiline) son aclaraciones    |
    | de funciones de la solucion, y aquellos con numeral (inline) son   |
    | de implementación.                                                 |
    |                                                                    |
     ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
     - Se agrego soporteMinimoOpcionales
     - Se agrego numero de reglas al principio, antes de la presentacion de las reglas resultantes
     - Se modifico apriori
     - Se modifico formato de reglas, ahora es [[antecedente],[consecuente],soporte,confianza]
     - Se modifico la presentacion de las reglas se ordena por confianza, soporte y cantidad de elementos
     - El soporte que se usa en la presentacion es del itemset con el que se genero la regla ej:
        si tenemos [1,2]->[3,4] el soporte que se usa es el del itemset [1,2,3,4]
'''

'''PASO1: GENERAR ITEMSETS FRECUENTES QUE SATISFAGAN EL SOPORTE MINIMO'''
'''Lee el archivo de entrada y lo mapea a una lista de listas'''
def leerDocumento(archivo):
    transacciones = open(archivo, 'r') # lee el archivo
    allTransac = []
    for linea in transacciones.readlines(): # lee linea por linea el archivo
        transaccion = list(map(int, linea.split())) # transforma cada linea del dataset en una lista
        transaccion.sort() # ordena la lista
        allTransac.append(transaccion) # agrega a la lista de todas las transacciones
    transacciones.close()
    return allTransac

'''Hace todas las combinaciones de k elementos sobre un subset'''
def subsets(arr, k):
    return chain(*[combinations(arr, k)])

'''Genera los candidatos de orden k desdesde un conjunto de itemsets
frecuentes de orden k-1'''
def candidateGen(setActual, k):
    # paso de union
    # la carga ya se hizo en orden lexicografico, no hace falta ordenar aca
    ccx = [] # lista de candidatos
    ffx = []
    ffx = setActual # set de items frecuentes
    for f1 in ffx:
        item1 = f1[0]
        for f2 in ffx:
            # para que siempre vaya para adelante con la generacion
            # ejemplo que no compare item 1 con 2 y en otra iteracion 2 con 1
            if (ffx.index(f2) <= ffx.index(f1)):
                continue
            # comparo elemento a elemento en orden lexicografico por igualdad
            item2 = f2[0]
            agregar = False
            for i in range(0, len(item1)):
                if (item1[i] != item2[i]):
                    if (i == len(item1)-1):
                        pos = i
                        agregar = True
                    else:
                        break
            if agregar:
                # al inicio c esta vacio ya que va a iterar varias veces, sino se hace esto se va
                # a acoplar sobre la iteracion anterior
                c = []
                c.extend(item1)
                c.append(item2[pos])
                c.sort()
                if (contieneEnListas(c, ccx) == False):
                    ccx.append(c)
    # paso de poda, propiedad de clausura hacia abajo
    # borro los candidatos que no esten en F[k]
    for cx in ccx:
        # genero los posibles subsets de longitud k-1 de cada candidato
        # los genera en orden
        subs = subsets(cx, k-1)
        subs = list(subs) # convertimos el objeto en lista para iterarlo
        #list(subs)
        # y verifico que se encuentre en F[k]
        for subset in subs:
            sub = list(subset)
            quitar = True
            for itemSet in ffx:
                if (sub == itemSet[0]):
                    quitar = False
                    break
            if quitar:
                # en caso de que intente borrar uno que ya se haya borrado antes
                try:
                    ccx.remove(cx)
                except ValueError:
                    pass
    return ccx

'''Determina si una lista esta contenida dentro de una lista de listas'''
def contieneEnListas(listaContenida, listaContenedora):
    # listacontenedora vacia
    contiene = False
    for lista in listaContenedora:
        # si no esta vacia puede comparar pero inicia en verdadero
        # asi si itera todo los elementos de la contenida
        # va a devolver true porque contiene.
        contiene = True
        for contenido in listaContenida:
            if contenido not in lista:
                # si hay un elto que no contiene pone en falso y
                # va al siguiente set de la lista contenedora
                contiene = False
                break
        if contiene: return contiene
    return contiene

'''Determina si una lista esta contenida dentro de otra'''
def contiene(listaContenida, listaContenedora):
    for contenido in listaContenida:
        if contenido not in listaContenedora:
            return False
    return True

'''Considera que un itemset puede estar una unica vez en una transaccion.
Si un candidato satisface el soporte minimo lo acopla a la lista de itemsets frecuentes'''
def soporteMinimo(transacciones, candidatos, minSup, k):
    itemsFrecuentes = []
    f = [k, itemsFrecuentes] # es el f de iteracion k
    # Calculo del soporte de los candidatos
    for itemC in candidatos:
        cont = 0
        itemFrecuente = []
        for t in transacciones:
            if contiene(itemC, t): # se verifica si el itemC esta contenido dentro de la lista
                cont += 1
        # Verificacion de la satisfaccion de soporte minimo
        if (float(cont)/len(transacciones) >= minSup): # si el candidato satisface el soporte minimo es un item frecuente
            itemFrecuente = [itemC, cont]
            itemsFrecuentes.append(itemFrecuente)
    return f

''' Considera la que un intemset puede existir mas de una vez en una transaccion.
Si un candidato satisface el soporte minimo lo acopla a la lista de itemsets frecuentes'''
def soporteMinimoOpcionales(transacciones, candidatos, minSup, k):
    itemsFrecuentes = []
    f = [k, itemsFrecuentes]
    # por cada candidato se comprueba si satisfacen el soporte minimo
    # en principio se toma candidato a candidato
    for itemC in candidatos:
        cont = 0
        itemFrecuente = []
        # se pasa a verificar cuantas veces aparece el candidato en las transacciones
        for transaccion in transacciones:
            ant = 0
            # ant almacena la cantidad de veces que aparece el item anterior,
            # si tenemos [[1],[2] almacena las ocurrencias de 1
            for item in itemC:
                cant = 0
                # cuenta la cantidad de ocurrencias de un item
                for elemento in transaccion:
                    if item == elemento:
                        cant += 1
                # contT siempre almacena la cantidad de ocurrencias del item del itemset
                # con menor aparicion en una transaccion
                if cant != 0:
                    if ant == 0:
                        ant = cant
                        contT = cant
                    else:
                        if cant <= ant:
                            contT = cant
                        else: contT = ant
                else:
                    # si no se encuentra algun item del itemset actual se pasa a la siguiente transaccion
                    contT = 0
                    break
            cont += contT
            # se cuenta la cantidad de ocurrencias de un itemset en una misma transaccion
            # antes de pasar a la siguiente
        # Verificacion de la satisfaccion de la condicion de minimo soporte
        if (float(cont)/len(transacciones) >= minSup):
            itemFrecuente = [itemC, cont]
            itemsFrecuentes.append(itemFrecuente)
    return f

'''Obtener los items existentes en el dataset'''
def initPass(transacciones):
    itemSet = []
    for transaccion in transacciones:
        for item in transaccion:
            if item not in itemSet:
                itemSet.append(item)
    devolver = []
    for i in itemSet:
        devolver.append([i])
    return devolver

'''Main'''
def apriori (transacciones, minSup, minConf, tope, ms):
    c1 = initPass(transacciones) # cc=C candidatos
    # se verifica si el campo ms esta activo, si es asi es porque
    # el usuario requiere que se consideren todas las ocurrencias de un itemset en una transaccion
    # para esto se cambia el calculo del soporte
    if ms: f1 = soporteMinimoOpcionales(transacciones, c1, minSup, k=1)
    else: f1 = soporteMinimo(transacciones, c1, minSup, k=1)
    k = 2
    setActual = f1[1]
    # en todosF se guardan todos los ff, es decir es F
    todosF = dict()
    todosF.update({str(f1[0]): f1[1]})
    while (len(setActual) != 0):
        print '--------NUEVA ITERACION------' + str(k) + '------'
        ccx = candidateGen(setActual, k)
        if ms: setNuevo = soporteMinimoOpcionales(transacciones, ccx, minSup, k)
        else: setNuevo = soporteMinimo(transacciones, ccx, minSup, k)
        setActual = setNuevo[1]
        todosF.update({str(setNuevo[0]): setNuevo[1]})
        # la siguiente seccion se utiliza si el campo tope de la funcion opcional esta activo
        # si esta activo solo devuelva hasta la iteracion con los k == tope
        # ya que de esta forma se obtiene solo itemsets de hasta una cantidad de elementos
        # lo que conlleva a reglas de una determinada cantidad de elementos
        if k != 0:
            if k == tope:
                break
        k += 1
    return todosF






'''PASO2: GENERAR REGLAS QUE SATISFAGAN LA CONFIANZA MINIMA'''
'''Devuelve una regla en formato [[antecedente/s],[consecuente/s]]'''
def generarRegla(f, h):
    # se realiza una resta de conjuntos entre el itemset y el consecuente
    # para obtener el antecedente
    antecedente = set(f).difference(set(h))
    # se genera la regla
    regla = [list(antecedente), h]
    return regla

'''Genera los items que van a resultar consecuentes de las reglas con mas
de un consecuente. Es semejante al anterior, pero cambia el paso de poda'''
def candidateGenReglas(ff, hh):
    # paso de union
    ccx = [] # lista de candidatos
    ffx = []
    ffx = hh # set de items frecuentes
    for f1 in ffx:
        item1 = f1[0]
        for f2 in ffx:
            # para que siempre vaya para adelante con la generacion
            # ejemplo que no compare item 1 con 2 y en otra iteracion 2 con 1
            if (ffx.index(f2) <= ffx.index(f1)):
                continue
            # comparo elemento a elemento en orden lexicografico por igualdad
            item2 = f2[0]
            agregar = False
            for i in range(0, len(item1)):
                if (item1[i] != item2[i]):
                    if (i == len(item1)-1):
                        pos = i
                        agregar = True
                    else:
                        break
            if agregar:
                # inicio c vacia ya que va a iterar varias veces y sino se va a
                # appendear sobre la iteracion anterior
                c = []
                c.extend(item1)
                c.append(item2[pos])
                c.sort()
                if (contieneEnListas(c, ccx) == False):
                    ccx.append(c)
    # ccx contiene la lista de candidatos
    # Paso de poda, propiedad de clausura hacia abajo
    # Recordemos que el conjunto de itemsets F ya cumplio con la propiedad de clausura hacia abajo
    # cuando se realizo el primer paso del algoritmo: encontrar los itemsets frecuentes que satisfagan el soporte minimo
    resultado = [] # lista de items que cumpliran la propiedad de clausura hacia abajo
    if len(ccx) != 0:
        m = str(len(ccx[0])) # compruebo la longitud de algun candidato para conocer la longitud de todos
        for h in ccx: # por cada candidato verifico si cumple con la propiedad
            for f in ff[m]:
                if h == f[0]: # compruebo si existe dentro del conjunto de itemsets frecuentes, si hay alguno igual
                    resultado.append(h) # si existe satisface la propiedad de clausura hacia abajo y se acopla a la lista
                    break
    return resultado

'''Obtener la confianza de una regla'''
def confianza(ff, contF, reglaCandidata):
    k = str(len(reglaCandidata[0])) # cantidad de elementos del antecedente
    antecedentes = set(reglaCandidata[0])
    # busco en F[longitud k] un itemset igual al antecedente y ordeno por las dudas
    for f in ff[k]:
        if (set(f[0]) == antecedentes):
            antcant = f[1] # contador de cantidad de ocurrencias antecedente
            break
    # calculo del consecuente
    conf = float(contF)/antcant
    return conf

'''Genera reglas de mas de un consecuente'''
def apGenRules(ff, f, key, m, hh, minConf, reglas, n):
    # reglas es reglasX en genRules
    k = int(key)
    if ((k > m+1) and (len(hh) != 0)):
        # hhx genera los candidatos que se utilizaran como consecuentes para las reglas
        # hh = [[[1]],[[2]],[[3]],[[4]]] es una lista de lista de lista
        # la funcion candidateGenReglas que se utiliza aqui solo me devuelve solo una lista de listas
        # [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
        hhx = candidateGenReglas(ff, hh)
        hhy = []
        # hhy es una lista que posteriormente servira para transformar hhx en el formato adecuado
        # para igresar en candidateGenReglas
        # una vez obtenidos los itemsets, almacenados en hhx, que se utilizaran como consecuentes
        # se generan las reglas
        for h in hhx:
            regla = generarRegla(f[0], h)
            conf = confianza(ff, f[1], regla) # confianza(ff, f, reglaCandidata): #f[1] veces que se repite si lo divido por n tengo el soporte
            if conf >= minConf:
                soporte = float(f[1])/n # se calcula el soporte del itemset
                regla.append(soporte) # se acopla el soporte del itemset
                regla.append(conf) # se acopla la confianza de la regla
                reglas.append(regla) # se acopla la regla a la lista de reglas (reglasX en genRules)
                hhy.append([h]) # se da el formato [h] al elemento de hhx y se lo acopla a hhy
        m += 1
        apGenRules(ff, f, key, m, hhy, minConf, reglas, n) # genero recursivamente el resto
        # de las reglas, hasta que llegue un punto que sea vacio
    return reglas

'''Genera las reglas de un consecuente y las acopla con el conjunto de reglas'''
def genRules(itemsFrecuentes, minConf, n):
    reglas = []
    reglasX = [] # lista con reglas
    ff = itemsFrecuentes # formato { 'k' : [[itemset], contador] }
    for key in ff:
        if (int(key) >= 2): # como la llave es un string lo paso a entero sino no podria iterar de esta manera
            for f in ff[key]:
                hh1 = [] #lista de consecuentes de las reglas con solo un consecuente
                # en la iteracion cada item de f[0] sera un consecuente
                for consecuente in f[0]:
                    regla1consec = generarRegla(f[0],[consecuente]) # generamo una regla de un solo consecunte
                    # se acopla un elemento a la lista de consecuentes hh1,
                    # este formato es para que se pueda utilizar posteriormente en apGenRules
                    hh1.append([[consecuente]])
                    conf = confianza(ff, f[1], regla1consec) # se calcula la confianza de la regla
                    if (conf >= minConf):
                        soporte = float(f[1])/n # se calcula el soporte
                        regla1consec.append(soporte) # se acopla el soporte del itemset
                        regla1consec.append(conf) # se acopla la confianza de la regla
                        reglasX.append(regla1consec) # se acopla la reglade un consecuente a la lista de reglas
                # Aclaracion importante: reglasX contiene posteriormente todas las reglas
                # a apGenRules entonces se le pasa por parametro todo el conjunto de reglas
                # en genRules se generan solo las reglas de un consecuente, en apGenRules el resto
                # pero reglasX contiene todas las reglas
                # en apGenRules se le acoplan las reglas de mas de un consecuente
                # (que se generan solo con los itemsets frecuentes y h)
                # y en genRules las de un consecuente
                reglas = apGenRules(ff, f, key, 1, hh1, minConf, reglasX, n) # genero reglas de mas de un consecuente
                # ff es el diccionario con todos los Itemsets Frecuentes: F
                # f es un solo Itemset
                # key es el K
                # 1 es el m en la primera iteracion
                # hh1 es el H1 (lista de consecuentes de 1 elemento)
                # reglasX tiene todas las reglas generadas no solo de un consecuente
    return reglas

'''Esta funcion filtra las reglas para que devuelva aquellas
que contengan cierto elemento pasado por parametro'''
def filtroElementos(reglas, elementos):
    filtro = []
    noExiste = []
    # comprobacion de la existencia del elemento ingresado como parametro
    # se verifica si se encuentra como antecedente o consecuente de alguna de las reglas generadas
    for elemento in elementos:
        existe = False
        for regla in reglas:
            if (elemento in regla[0]) or (elemento in regla[1]):
                existe = True
                if regla not in filtro:
                    filtro.append(regla)
        if existe == False:
            noExiste.append(elemento)
    if len(filtro) == 0:
        archivo = open('reglas.txt', 'w')
        archivo.write('No hay reglas con los elementos:'+ str(elementos)+'.\n')
        archivo.close()
    return [filtro,noExiste]

'''Funcion que genera el archivo con los resultados'''
def resultadosg(reglas, minSup, minConf, nombre, elementos, noExiste):
    archivo = open(nombre,'w') # para generar el archivo
    archivo.write('------------------------ RESULTADOS ---------------------------\n')
    archivo.write('\n--- Minimo Soporte: '+ minSup)
    archivo.write(' ---')
    archivo.write('--- Minima Confianza: '+ minConf + ' ---\n')
    archivo.write('\n')
    if elementos != 'nada':
        archivo.write('Elementos Buscados: '+str(elementos)+ '\n\n')
        if len(noExiste) != 0:
            archivo.write('Aviso: no se encontraron reglas con los elementos: '+str(noExiste)+'\n\n')
    archivo.write('Se generaron: ' + str(len(reglas)) + ' reglas\n\n')
    archivo.write('---------------------------- REGLAS ------------------------------\n\n')
    archivo.write('Regla #: antecedente --> consecuente        soporte - confianza\n')
    archivo.write('\n')
    i = 1
    for regla in reglas:
        pre = regla[0]
        post = regla[1]
        soporte = regla[2]
        conf = regla[3]
        # impresion en pantalla
        regla = "Regla %s: %s --> %s        S(%.3f) - C(%.3f)" % (i, pre, post, soporte, conf)
        # agregar al archivo
        archivo.write(regla + '\n') #
        i += 1
    if (i==1):
        archivo.write('\n\n\n\n\n No fue posible generar reglas con los parametros especificados ')
    archivo.close()
    return os.path.abspath('reglas.txt')

'''Punto de acceso al algoritmo apriori, llamada desde el cliente a esta funcion'''
def inicio(ds, sup, conf, longRule, rulesOfElements, repetidos):
    if (repetidos == False):
        ms = False
    else:
        ms = True
    if (longRule == ""): longRule = 0
    if (rulesOfElements == ""):
        elementos = 'nada'
    else:
        elementos = map(int, (rulesOfElements).split())
    dset = leerDocumento(ds)
    ff = apriori(dset, float(sup), float(conf), int(longRule), ms)
    n = len(dset)
    r = genRules(ff, float(conf), n)
    # ordeno de mayor a menor por confianza, soporte y tambien de menor a mayor por longitud de regla
    r.sort(key=lambda x:(x[2], x[3], -len(x[0]), -len(x[1])), reverse=True)
    noExiste = []
    if elementos != 'nada':
        filtro = filtroElementos(r, elementos)
        r = filtro[0]
        noExiste = filtro[1]
    return resultadosg(r, str(sup), str(conf), 'reglas.txt', elementos, noExiste)
