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
import threading

# tamanho da lista
n = 100
arquivo = "wordlist.txt"
verbose = True
# veja a definicao de congruencia linear
a = 1
# incremento inicial
c = 5
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
	if 			velocidade < 1e3: velocidade = "%.3f l/s" % velocidade
	elif  1e3 < velocidade < 1e6: velocidade = "%.2f K/s" % (velocidade/1e3)
	elif  1e6 < velocidade < 1e9: velocidade = "%.2f M/s" % (velocidade/1e6)
	else:						  velocidade = "%.2f G/s" % (velocidade/1e9)
	stdout.write("\r%.2f%%. Tempo estimado: %s " % (progresso, estimativa))
	stdout.write("@ %s" % velocidade)
	stdout.write("\t(CTRL-\ para abortar)\r")

def main():
	"""Onde a mágica acontece. :D"""

	# Busca c tal que c e n sejam coprimos
	global a, c, n
	tamanho = 0
	if argv[1:]:
		tamanho = int(argv[1])
		n = 10 ** tamanho
	c = int(n / 4)
	if not pipe: print("Buscando o menor coprimo de %d e %d..." % (n, c))
	while mdc(n, c) != 1: c += 1
	if not pipe: print("Encontrado: " + str(c))

	# Calcula a-1 como produto dos fatores primos nao repetidos de n
	for i in fatores(n): a *= i
	# Segundo Knuth, deve haver a condicao abaixo
	if (n % 4) == 0: a = a * 4
	# a finalmente calculado
	a += 1
	if not pipe: print("a = %d" % a)
	x, inicio = 1, 1
	if not pipe: print("Gerando lista... ")

	with open(arquivo, "w") as wordlist:
		if pipe: wordlist = stdout
		for i in range(n):
			try:
				# if verbose == True:
				# 	if random() < 1e-7:
				# 		raise(KeyboardInterrupt)
				# lista.append(x)
				linha = str(x).zfill(tamanho)
				wordlist.write(linha + '\n')
				x = (a*x + c) % n
			# Status
			except KeyboardInterrupt as e:
				status(i)
				continue

		print('')
			# if x == inicio: break
	print("Concluído em %s" % timedelta(seconds=int(time()-start)))




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
