dicP = dict()
dicC = {'Horitzontal': {}, 'Vertical': {}}
cross = list()


archivo = open("MaterialsPractica/diccionari_CB_v3.txt", "rt")

for linia in archivo:
    linia = linia.strip('\n')
    if len(linia) in dicP:
        dicP[len(linia)].append(linia)
    else:
        dicP[len(linia)] = [linia]


archivo = open("MaterialsPractica/crossword_CB_v3.txt", "rt")

for l, linia in enumerate(archivo):
    cross.append(list())
    linia = linia.strip('\n')
    for char in linia:
        if char != '	':
            cross[l].append(char)

minim = min(dicP.keys())