def converte_intervalos_em_arvore(intervalos):
	arvore = []
	for i in intervalos:
		arvore.append({'filhos': [], 'intervalo': i})
	intervalos = sorted(intervalos, key=lambda k: (k[1]-k[0]), reverse=True)
	for i, inter in enumerate(intervalos):
		arvore[i]['intervalo'] = intervalos[i]
		cont = i-1
		while cont >= 0:
			if intervalos[cont][0] <= intervalos[i][0] and intervalos[cont][1] >= intervalos[i][1]:
				arvore[cont]['filhos'].append(i)
				break
			cont -= 1
	return arvore

lista_teste = [(13, 16), (11, 15), (0, 100), (10, 20), (30, 40)]
print(converte_intervalos_em_arvore(lista_teste))