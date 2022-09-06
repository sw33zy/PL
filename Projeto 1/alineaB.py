import re

def int_to_Roman(num):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
            ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
            ]
        roman_num = ''
        i = 0
        while  num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        return roman_num

f = open('processos.xml')

nomes = {}
apelidos = {}
seculo = 0
for line in f:
   
    if res2 := re.search(r'<data>((.|\n)*)<\/data>',line) :

        if int((re.split(r'-', res2.group(1))[0])) % 100 != 0 :
            seculo = int((re.split(r'-', res2.group(1))[0]))//100 +1
        else:
            seculo = int((re.split(r'-', res2.group(1))[0]))//100
        
    if res := re.search(r'<nome>((.|\n)*)<\/nome>',line) :
        nome = re.search(r'^[A-Za-z]+', res.group(1)).group(0)
        apelido = re.search(r'[A-Za-z]+$', res.group(1)).group(0)

        

        if (nome,seculo) in nomes.keys():
            nomes[nome,seculo] += 1
        else:
            nomes[nome,seculo] = 1

        if (apelido,seculo) in apelidos.keys():
            apelidos[apelido,seculo] += 1
        else:
            apelidos[apelido,seculo] = 1

nomes = dict(sorted(nomes.items(), 
        key=lambda p: (p[0][1], p[1]),reverse=True))
apelidos = dict(sorted(apelidos.items(), 
        key=lambda p: (p[0][1], p[1]),reverse=True))
freqnomes = []
freqapelidos = []


def freqs(lista,listafreq):
    sec = list(lista.keys())[0][1]
    i = 0
    for n in lista:
    
        if((sec == n[1])):
            if(i < 5):
                listafreq.append((n[0],lista[n]))
                i+=1
            else:
                sec -=1
                i=0

freqs(nomes,freqnomes)
freqs(apelidos,freqapelidos)

def topfreq(string, listafreq):
    sec = list(nomes.keys())[0][1]
    i=0
    print(f'{string}')
    print(f'Século {int_to_Roman(sec)}:')
    for f in listafreq:
        
            
        if(i < 5):
            s = '\tNome: {:11} Frequência: {:}'.format(f[0],f[1])
            print(s)
            i+=1
        else:
            sec-=1
            print(f'\nSéculo {int_to_Roman(sec)}:')
            s = '\tNome: {:11} Frequência: {:}'.format(f[0],f[1])
            print(s)
            i=1

topfreq('-------------------------------------------------\n{:20} Nomes\n-------------------------------------------------'.format(' '), freqnomes)
topfreq('-------------------------------------------------\n{:18} Apelidos\n-------------------------------------------------'.format(' '), freqapelidos)


