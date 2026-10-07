def backtracking(tasques, index, matriu, visitats):
    if index == len(tasques):
        return True
    direccio = tasques[index][0]
    x = tasques[index][1]
    allargada = tasques[index][2]
    y = tasques[index][3]
    if allargada in dicP:
        for p in dicP[allargada]:
            if p not in visitats:
                if direccio == 'H':
                    copia = list(matriu[x])
                    valida = posarParaulaH(p,x,y, matriu)
                else:
                    copia = [matriu[i][y] for i in range(len(matriu))]
                    valida = posarParaulaV(p,x,y,matriu)
                if valida:
                    visitats.append(p)
                    if backtracking(tasques, index+1, matriu, visitats):
                        return True
                    visitats.pop()
                if direccio =='H':
                    matriu[x] = list(copia)
                else:
                    for i in range(len(matriu)):
                        matriu[i][y] = copia[i]

    return False


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

dicC = {'Horitzontal': {}, 'Vertical': {}}
dicP = dict()
cross = list()

archivo1 = open("MaterialsPractica/dicP_CB_v3.txt", "rt")
for linia in archivo1:
    linia = linia.strip('\n')
    if len(linia) in dicP:
        dicP[len(linia)].append(linia)
    else:
        dicP[len(linia)] = [linia]
archivo1.close()

archivo2 = open("MaterialsPractica/crossword_CB_v3.txt", "rt")

for l, linia in enumerate(archivo2):
    cross.append(list())
    linia = linia.strip('\n')
    for char in linia:
        if char != '	':
            cross[l].append(char)
archivo2.close()

minim = min(dicP.keys())

for l, linia in enumerate(cross):
    index = 0
    resultats = []
    s = 0

    for char in linia:
        if char == '0':
            s += 1
        else:
            if s >= minim:
                resultats.append([s, index-s])
            s = 0
        index += 1

    if s >= minim:
        resultats.append([s, index-s])

    dicC['Horitzontal'][l] = resultats

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

tasques = []
for l, forats in dicC['Horitzontal'].items():
    for f in forats:
        tasques.append(('H', l, f[0], f[1])) 
        
for c, forats in dicC['Vertical'].items():
    for f in forats:
        tasques.append(('V', f[1], f[0], c)) 

visitats = []
if backtracking(tasques, 0, cross, visitats):
    print("Solució trobada")
    for fila in cross:
        print(" ".join(fila))
else:
    print("No s'ha trobat solució.")
