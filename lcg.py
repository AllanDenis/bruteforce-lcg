# Itera pseudoaleatoriamente sobre uma sequencia com indices conhecidos; ou seja, implementa um gerador de congruencia linear (LCG)

# tamanho da lista
n = 100
# se for muito grande, mude mostrar para 'n'
mostrar = 's'
# veja a definicao de congruencia linear
a = 1
# incremento inicial
c = 5

# descomente a linha abaixo se for executar localmente
#arquivo = open("lista.lst", "w")

import math
import time

# Retorna o maximo divisor comum positivo de a e b
def mdc(a, b):
	while b: a, b = b, a % b
	return abs(a)

# Retorna a fatoracao de n
def fac(n):
	incremento = lambda x: int(1 + x*4 - (x/2)*2)
	maxq = math.floor(math.sqrt(n))
	d = 1
	q = n % 2 == 0 and 2 or 3 
	while q <= maxq and n % q != 0:
		q = incremento(d)
		d += 1
	fatoracao = []
	if q <= maxq:
		fatoracao.extend(fac(n//q))
		fatoracao.extend(fac(q)) 
	else: fatoracao = [n]
	return set(fatoracao)

start = time.time()

# Busca c tal que c e n sejam coprimos 
print("Buscando o menor coprimo de n (" + str(n) + ")...")
while mdc(n, c) != 1: c = c + 1
print("Encontrado: " + str(c))

# Calcula a-1 como produto dos fatores primos nao repetidos de n
print("Calculando a...")
for i in fac(n): a = a * i

# Segundo Knuth, deve haver a condicao abaixo
if (n % 4) == 0: a = a * 4

# a finalmente calculado
a = a + 1
print("Calculado: " + str(a))

x, inicio = 1, 1
lista = []
print("Gerando lista...")
while True:
        # descomente a linha abaixo se for executar localmente
	#arquivo.write(str(x).zfill(8) + '\n')
	lista.append(x + 1)
	#print(str(x + 1))
	x = (a * x + c) % n
	if x == inicio: break

# Teste final
resultado = "A lista contem todos os elementos em ordem pseudoaleatoria?"
if(str(len(lista) == lista[-1] == n)):
	resultado = resultado + " Sim. :D"
else:
	resultado = resultado + "Nao :("
print(resultado)
print("Tempo total: %ss" % (time.time() - start))
print("n, a, c = " + str(n) + ",  " + str(a) + ", " + str(c))
# descomente a linha abaixo se for executar localmente
# mostrar = input("A lista possui " + str(len(lista)) + " elementos. Deseja ver todos eles? [s/n] ")
if mostrar == 's':
	for i in range(len(lista)):
		print(str(i + 1) + ": " + str(lista[i]));
# descomente a linha abaixo se for executar localmente
#input("Fim. Pressione enter.")