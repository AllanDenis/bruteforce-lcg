#!/usr/bin/python

# -*- coding: utf-8 -*-

"""
	Itera pseudoaleatoriamente sobre uma sequencia com indices conhecidos;
	ou seja, implementa um gerador de congruencia linear (LCG)
"""

from math import floor, sqrt, log10
from random import random
from sys import argv, stdout
from time import time
from datetime import timedelta
from pprint import pprint
import threading

# tamanho da lista
n = 100
arquivo = "wordlist.csv"
verbose = True
# veja a definicao de congruencia linear
a = 1
# incremento inicial
c = n
lista = []
pipe = True if '-p' in argv else False

def mdc(a, b):
	"""Retorna o maximo divisor comum positivo de a e b"""
	while b: a, b = b, a % b
	return abs(a)


def fatores(n):
	"""Retorna os fatores primos de n"""
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


def status(i):
	"""Exibe o progresso da execução."""
	velocidade = i / (time() - start)
	estimativa = (n-i)/velocidade
	estimativa = timedelta(seconds=int(estimativa))
	progresso = 100 * (i/n)

	# Legível para humanos
	fator = int(log10(velocidade) / 3)
	kmg = '#KMGT' #kilo, mega, giga, tera...
	stdout.write("\r%.2f%%. Tempo estimado: %s " % (progresso, estimativa))
	stdout.write("@ %.0f %s/s" % (velocidade, kmg[fator]))
	stdout.write("\t(CTRL \ para abortar)\r")


def main():
	"""Onde a mágica acontece. :D"""

	# Busca c tal que c e n sejam coprimos
	global a, c, n
	tamanho = 10 ** 8
	try:
		tamanho = int(argv[argv.index('-p') + 1])
		n = 10 ** tamanho
	except ValueError as e:
		pass
	while mdc(n, c) != 1: c += 1

	# Calcula a-1 como produto dos fatores primos nao repetidos de n
	for i in fatores(n): a *= i
	# Segundo Knuth, deve haver a condicao abaixo
	if (n % 4) == 0: a *= 4
	# a finalmente calculado
	a += 1
	x = inicio = 1
	if not pipe: print("Gerando lista... ")

	wordlist = stdout if pipe else open(arquivo, "w")
	for i in range(n):
		try:
			linha = str(x).zfill(tamanho)
			wordlist.write("%s\n" % linha)
			x = (a*x + c) % n
		# Status
		except KeyboardInterrupt as e:
			status(i)
			continue

	if not pipe:
		wordlist.close()
		print("Concluído em %s" % timedelta(seconds=int(time()-start)))


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
			# Teste


if __name__ == '__main__':
	start = time()
	main()
	# lcg_test()
