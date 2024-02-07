# Lista original fornecida pelo usuário
lista_original = [((1,0),(0,1)), ((3,4),(1,4)), ((1,0),(3,4))]

# Ordenando a lista com base na soma dos elementos de cada tupla
lista_ordenada = sorted(lista_original, key=lambda par: (par[0][0] + par[0][1], par[1][0] + par[1][1]))

print(lista_ordenada)
