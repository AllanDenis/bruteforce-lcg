#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
	Itera pseudoaleatoriamente sobre uma sequencia com indices conhecidos;
	ou seja, implementa um gerador de congruencia linear (LCG)
"""

from math import floor, sqrt
from random import random
from sys import argv, stdout
from time import time
import threading

# tamanho da lista
n = 100
arquivo = "wordlist.txt"
# Para n muito grande, mude mostrar para False
verbose = True
# veja a definicao de congruencia linear
a = 1
# incremento inicial
c = 5
lista = []

# Retorna o maximo divisor comum positivo de a e b
def mdc(a, b):
	while b: a, b = b, a % b
	return abs(a)


# Retorna os fatores primos de n
def fatores(n):
	incremento = lambda x: int(1 + x*4 - (x/2)*2)
	maxq = floor(sqrt(n))
	d = 1
	q = n % 2 == 0 and 2 or 3
	while q <= maxq and n % q != 0:
		q = incremento(d)
		d += 1
	fatoracao = []
	if q <= maxq:
		fatoracao.extend(fatores(n//q))
		fatoracao.extend(fatores(q))
	else: fatoracao = [n]
	return set(fatoracao)


def main():
	"""Onde a mágica acontece. :D"""

	# Busca c tal que c e n sejam coprimos
	global a, c, n
	if argv[1:]: n = 10 ** int(argv[1])
	c = int(n / 4)
	print("Buscando o menor coprimo de %d e %d..." % (n, c))
	while mdc(n, c) != 1: c += 1
	print("Encontrado: " + str(c))

	# Calcula a-1 como produto dos fatores primos nao repetidos de n
	for i in fatores(n): a *= i
	# Segundo Knuth, deve haver a condicao abaixo
	if (n % 4) == 0: a = a * 4
	# a finalmente calculado
	a = a + 1
	print("a = %d" % a)
	x, inicio = 1, 1
	print("Gerando lista... ")
	with open(arquivo, "w") as wordlist:
		tamanho = len(str(n))
		for i in range(n):
		    # descomente a linha abaixo se for executar localmente
			linha = str(x).zfill(tamanho)
			wordlist.write(linha + '\n')
			lista.append(x)
			x = (a*x + c) % n
			# if x == inicio: break
	print("Pronto.")

# Teste
def lcg_test():
	if len(lista) == 0:
		print("Lista vazia. O teste não rodou.")
		return
	print("Testando...")
	if len(lista) == n and sorted(lista) == list(range(n)):
		print("Funcionou! :D")
	else:
		print("Não funcionou. :(")
	print("Tempo total: %.3f s" % float(time() - start))
	print("n, a, c = " + str(n) + ",  " + str(a) + ", " + str(c))
	verLista = input("A lista possui " + str(len(lista)) + " elementos. Deseja vê-los? [s/n] ")
	if verLista.lower() == 's':
		for i in range(len(lista)):
			print(str(i + 1) + ": " + str(lista[i]));


if __name__ == '__main__':
	start = time()
	main()
	# lcg_test()
