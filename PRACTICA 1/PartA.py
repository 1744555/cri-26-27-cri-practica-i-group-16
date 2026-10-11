import time
from pathlib import Path


def posarParaulaH(p, x, y, matriu):
    it = y
    for char in p:
        if matriu[x][it] == char or matriu[x][it] == '0':
            matriu[x][it] = char
            it += 1
        else:
            return False
    return True


def posarParaulaV(p, x, y, matriu):
    it = x
    for char in p:
        if matriu[it][y] == char or matriu[it][y] == '0':
            matriu[it][y] = char
            it += 1
        else:
            return False
    return True


def actualitzarDominis(espais, cross, dicP, visitats, paraula):
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

                    if i == forat[2]:
                        domini = True
                        break

            if not domini:
                return False
    return True



def backtracking(espais, index, matriu, visitats):
    if index == len(espais):
        return True

    direccio, x, llargada, y = espais[index]

    if llargada not in dicP:
        return False

    if direccio == 'H':
        copia = list(matriu[x])
        posar_paraula = posarParaulaH
    else:
        copia = [matriu[i][y] for i in range(len(matriu))]
        posar_paraula = posarParaulaV

    for p in dicP[llargada]:
        if p in visitats:
            continue

        valida = posar_paraula(p, x, y, matriu)

        if valida and actualitzarDominis(espais, matriu, dicP, visitats, p):
            visitats.append(p)

            if backtracking(espais, index + 1, matriu, visitats):
                return True

            visitats.pop()

        if direccio == 'H':
            matriu[x] = list(copia)
        else:
            for i in range(len(matriu)):
                matriu[i][y] = copia[i]

    return False


#carreguem fitxerrs PART A

dicC = {'Horitzontal': {}, 'Vertical': {}}
dicP = dict()
cross = list()

# lectura del diccionari reduit 
MAX_PARAULES = 10000 
comptador = 0

ruta = Path(__file__).parent / "MaterialsPractica" / "diccionari_A.txt"
with open(ruta, "rt", encoding="latin-1") as archivo1:
    for linia in archivo1:
        if comptador >= MAX_PARAULES:
            break
        linia = linia.strip('\n')
        if len(linia) in dicP:
            dicP[len(linia)].append(linia)
        else:
            dicP[len(linia)] = [linia]
        comptador += 1

print(f"Nombre de paraules carregades: {comptador}")

# llegim tauler
ruta2 = Path(__file__).parent / "MaterialsPractica" / "crossword_A.txt"
with open(ruta2, "rt", encoding="latin-1") as archivo2:
    for l, linia in enumerate(archivo2):
        cross.append(list())
        linia = linia.strip('\n')
        for char in linia:
            if char != '\t':
                cross[l].append(char)

minim = min(dicP.keys())

# Horitzontals
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

# Verticals
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

# Creació de la llista de variables
espais = []
for l, forats in dicC['Horitzontal'].items():
    for f in forats:
        espais.append(('H', l, f[0], f[1]))

for c, forats in dicC['Vertical'].items():
    for f in forats:
        espais.append(('V', f[1], f[0], c))


visitats = []
inici = time.perf_counter()

if backtracking(espais, 0, cross, visitats):
    print("Solució trobada:")
    for fila in cross:
        print(" ".join(fila))
else:
    print("No s'ha trobat solució.")

fi = time.perf_counter()
print(f"\nTemps d'execució del Backtracking: {fi - inici:.6f} segons")