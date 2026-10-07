def backtracking(espais, index, matriu, visitats):
    #Comprovem si hem omplert tot l'encreuat
    if index == len(espais):
        return True

    #Assignem la informació de l'espai
    direccio = espais[index][0] #Tindrem 'H' = horitzontal i 'V' = vertical
    x = espais[index][1] #Fila on comença l'espai
    allargada = espais[index][2] #longitud de l'espai = nombre de lletres
    y = espais[index][3] #columna on comença l'espai

    #Comprovem si el diccionari té paraules amb aquesta longitud
    if allargada in dicP:
        for p in dicP[allargada]:
            #Si n'hi ha ens assegurem de no fer servir una paraula que ja està posada al tauler
            if p not in visitats:
                if direccio == 'H':
                    #Fem una copia de la fila per poder desfer els canvis en cas de que aquesta paraula no porta a una solució
                    copia = list(matriu[x])
                    valida = posarParaulaH(p,x,y, matriu)

                else:
                    #Fem una copia de la columna per poder desfer els canvis en cas de que aquesta paraula no porta a una solució
                    copia = [matriu[i][y] for i in range(len(matriu))]
                    valida = posarParaulaV(p,x,y,matriu)

                if valida:
                    #Si la paraula es valida la marquem com a utilitzada
                    visitats.append(p)

                    #avancem al següent espai
                    if backtracking(espais, index+1, matriu, visitats):
                        return True

                    #En cas de que el camí no sigui valid, el desfem
                    visitats.pop()

                #I restaurem la matriu segons la direcció
                if direccio =='H':
                    matriu[x] = list(copia)

                else:
                    for i in range(len(matriu)):
                        matriu[i][y] = copia[i]

    #Si cap paraula funciona, aquesta branca no te solució
    return False


def posarParaulaH(p, x, y, matriu):
    #Funció per col·locar una paraula en horitzontal. Comprova que cada lletra encaixi amb l'espai buit o amb la lletra que hi ha.
    it = y
    for char in p:
        if matriu[x][it] == char or matriu[x][it] == '0':
            matriu[x][it] = char
            it += 1
        else:
            return False
    return True



def posarParaulaV(p, x, y, matriu):
    #Funció per col·locar una paraula en vertical aplicant la mateixa lògica que abans
    it = x
    for char in p:
        if matriu[it][y] == char or matriu[it][y] == '0':
            matriu[it][y] = char
            it += 1
        else:
            return False
    return True


#Estructures de dades per emmagatzemar els espais, el diccionari i la matriu de l'encreuat
dicC = {'Horitzontal': {}, 'Vertical': {}}
dicP = dict()
cross = list()

#Lectura el diccionari de paraules i agrupar-ho per longitud, amb això facilitem la cerca
archivo1 = open("MaterialsPractica/diccionari_CB_v3.txt", "rt")
for linia in archivo1:
    linia = linia.strip('\n')
    if len(linia) in dicP:
        dicP[len(linia)].append(linia)
    else:
        dicP[len(linia)] = [linia]
archivo1.close()

#Lectura del fitxer que conté l'estructura inicial de l'encreuat
archivo2 = open("MaterialsPractica/crossword_CB_v3.txt", "rt")
for l, linia in enumerate(archivo2):
    cross.append(list())
    linia = linia.strip('\n')
    for char in linia:
        if char != '\t':
            cross[l].append(char)
archivo2.close()

#obtenim la mida de la paraula més petita per descartar espais massa petits
minim = min(dicP.keys())

#Anàlisis del tauler per trobar els espais horitzontals
for l, linia in enumerate(cross):
    index = 0
    resultats = []
    s = 0 #comptem les caselles buides consecutives

    for char in linia:
        if char == '0':
            s += 1
        else:
            #Si l'espai es mes gran que la paraula més petita el guardem
            if s >= minim:
                resultats.append([s, index-s])
            s = 0
        index += 1
    #Comprovem si l'espai arriba al final de la linia
    if s >= minim:
        resultats.append([s, index-s])

    dicC['Horitzontal'][l] = resultats

#Anàlisis del tauler per trobar espais verticals
for c in range(len(cross[0])):
    index = 0
    resultats = []
    s = 0
    for l in range(len(cross)):
        if cross[l][c] == '0':
            s += 1
        else:
            if s >= minim:
                resultats.append([s, index-s])
            s = 0
        index += 1
    if s >= minim:
        resultats.append([s, index-s])
    if resultats:
        dicC['Vertical'][c] = resultats

#llista que emmagatzema els espais
espais = []
for l, forats in dicC['Horitzontal'].items():
    for f in forats:
        #Els parametres són: Direcció, Fila, Longitud, Columna d'inici.
        espais.append(('H', l, f[0], f[1])) 
        
for c, forats in dicC['Vertical'].items():
    for f in forats:
        #Els parametres són: Direcció, Fila d'inici, Longitud, Columna
        espais.append(('V', f[1], f[0], c)) 

#Algorisme recursiu començant per l'espai 0
visitats = []
if backtracking(espais, 0, cross, visitats):
    print("Solució trobada")

    #Imprimeix la matriu resultant amb la solució
    for fila in cross:
        print(" ".join(fila))
else:
    print("No s'ha trobat solució.")
