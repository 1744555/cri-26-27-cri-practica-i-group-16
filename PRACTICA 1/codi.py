def backtracking(cross, visitats):
    if not visitats.empty():
        esborra = visitats[len(visitats) - 1]
        p = []
        for char in esborra:
            p.append(char)


def posarParaulaH(allargada, visitats, x, y, matriu):
    paraulaCorrecte = False
    copia = matriu[x]

    for p in dicP[allargada]:
        if p not in visitats:
            iterador = y
            for char in p:
                if matriu[x][iterador] == char or matriu[x][iterador] == '0':
                    matriu[x][iterador] = char
                    paraulaCorrecte = True
                    iterador += 1

                else:
                    paraulaCorrecte = False
                    matriu[x] = copia
                    break

            if paraulaCorrecte:
                visitats.append(p)
                break

    return paraulaCorrecte


def posarParaulaV(allargada, visitats, x, y, matriu):
    paraulaCorrecte = False
    copia = matriu

    for p in dicP[allargada]:
        if p not in visitats:
            iterador = x
            for char in p:
                if matriu[iterador][y] == char or matriu[iterador][y] == '0':
                    matriu[iterador][y] = char
                    paraulaCorrecte = True
                    iterador += 1

                else:
                    paraulaCorrecte = False
                    for i in range(len(matriu)):
                        matriu[i][y] = copia[i][y]

                    break

            if paraulaCorrecte:
                visitats.append(p)
                break

    return paraulaCorrecte

dicC = {'Horitzontal': {}, 'Vertical': {}}
dicP = dict()
cross = list()

archivo1 = open("MaterialsPractica/diccionari_CB_v3.txt", "rt")
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

dicC['Vertical'][0]: resultats