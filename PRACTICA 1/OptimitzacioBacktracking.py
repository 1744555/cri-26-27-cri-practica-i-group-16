
from pathlib import Path

def posarParaulaH(p, x, y, matriu):
    #Volem colocar una paraula en horitzontal
    # Comprovem que cada lletra encaixi amb l'espai buit o amb la lletra que hi ha
    it = y
    for char in p:
        if matriu[x][it] == char or matriu[x][it] == '0':
            matriu[x][it] = char
            it += 1
        else:
            return False
    return True


def posarParaulaV(p, x, y, matriu):
    #Volem colocar una paraula en vertical
    # Comprovem que cada lletra encaixi amb l'espai buit o amb la lletra que hi ha
    it = x
    for char in p:
        if matriu[it][y] == char or matriu[it][y] == '0':
            matriu[it][y] = char
            it += 1
        else:
            return False
    return True


def actualitzarDominis(espais, cross, dicP, visitats, paraula):
    #Es tracta de comprovar si tots els forats que queden tenen almenys una paraula valida
    for forat in espais:
        domini = False

        if '0' in cross[forat[1]][forat[3]]:
            for p in dicP[forat[2]]:
                if p not in visitats and p != paraula:
                    i = 0
                    for char in p:
                        if forat[0] == 'V':
                            if cross[forat[1] + i][forat[3]] != char and cross[forat[1] + i][forat[3]] != '0':
                                break
                        else:
                            if cross[forat[1]][forat[3] + i] != char and cross[forat[1]][forat[3] + i] != '0':
                                break
                        i += 1
                #si tota la paraula encaixa amb el forat, aquest forat té almenys una paraula que hi pot anar
                    if i == forat[2]:
                        domini = True
                        break
            #sino, podem la branca
            if not domini:
                return False

    return True


def backtracking(espais, index, matriu, visitats):
    # si omplim tots els espais
    if index == len(espais):
        return True

    # "Desempaquetament" de la variable
    direccio, x, llargada, y = espais[index]

    # acaba funcio si no hi ha cap paraula d'aquesta longitud al diccionari
    if llargada not in dicP:
        return False

    # part optimitzada: la copia del tauler i la funció a utilitzar fora del bucle
    if direccio == 'H':
        copia = list(matriu[x])
        posar_paraula = posarParaulaH
    else:
        copia = [matriu[i][y] for i in range(len(matriu))]
        posar_paraula = posarParaulaV

    # recorrem les paraules candidates d'aquesta longitud
    for p in dicP[llargada]:
        if p in visitats:
            continue

        # provem de colocar la paraula utilitzant la referència (posar_paraula)
        valida = posar_paraula(p, x, y, matriu)

        # Forward Checking i crida recursiva
        if valida and actualitzarDominis(espais, matriu, dicP, visitats, p):
            visitats.append(p)

            if backtracking(espais, index + 1, matriu, visitats):
                return True

            visitats.pop()

        # Restaurem la matriu des de la copia (feta fora del bucle)
        if direccio == 'H':
            matriu[x] = list(copia)
        else:
            for i in range(len(matriu)):
                matriu[i][y] = copia[i]

    return False


dicC = {'Horitzontal': {}, 'Vertical': {}}
dicP = dict()
cross = list()

# Lectura del diccionari
ruta = Path(__file__).parent / "MaterialsPractica" / "diccionari_CB_v3.txt"
with open(ruta, "rt") as archivo1:
    for linia in archivo1:
        linia = linia.strip('\n')
        if len(linia) in dicP:
            dicP[len(linia)].append(linia)
        else:
            dicP[len(linia)] = [linia]

# Lectura de l'esquema de l'encreuat
ruta2 = Path(__file__).parent / "MaterialsPractica" / "crossword_CB_v3.txt"
with open(ruta2, "rt") as archivo2:
    for l, linia in enumerate(archivo2):
        cross.append(list())
        linia = linia.strip('\n')
        for char in linia:
            if char != '\t':
                cross[l].append(char)

minim = min(dicP.keys())

# possibles spais horitzontals
for l, linia in enumerate(cross):
    index = 0
    resultats = []
    s = 0
    for char in linia:
        if char == '0':
            s += 1
        else:
            if s >= minim:
                resultats.append([s, index - s])
            s = 0
        index += 1
    if s >= minim:
        resultats.append([s, index - s])
    dicC['Horitzontal'][l] = resultats

#posisbles espais verticals
for c in range(len(cross[0])):
    index = 0
    resultats = []
    s = 0
    for l in range(len(cross)):
        if cross[l][c] == '0':
            s += 1
        else:
            if s >= minim:
                resultats.append([s, index - s])
            s = 0
        index += 1
    if s >= minim:
        resultats.append([s, index - s])
    if resultats:
        dicC['Vertical'][c] = resultats

# creació de la llista conjunta d'espais (variables del problema)
espais = []
for l, forats in dicC['Horitzontal'].items():
    for f in forats:
        espais.append(('H', l, f[0], f[1]))

for c, forats in dicC['Vertical'].items():
    for f in forats:
        espais.append(('V', f[1], f[0], c))
"""
# Execució de l'algorisme
visitats = []
if backtracking(espais, 0, cross, visitats):
    print("Solució trobada:")
    for fila in cross:
        print(" ".join(fila))
else:
    print("No s'ha trobat solució.")
"""

#prova per veure el temps d'execució del backtracking
import time

visitats = []
inici = time.perf_counter()  

if backtracking(espais, 0, cross, visitats):
    print("Solució trobada")

fi = time.perf_counter()    

temps_total = fi - inici
print(f"Temps d'execució del Backtracking: {temps_total:.6f} segons")

