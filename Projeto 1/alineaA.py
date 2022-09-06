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

anos = {}
ano_menor = '~'
ano_maior = ''
seculos = set()
for line in f:
    if res := re.search(r'<data>((.|\n)*)<\/data>',line) :
        ano = re.split(r'-', res.group(1))[0]
        data = res.group(1)

        if int(ano)% 100 != 0 :
            seculos.add(int(ano)//100 + 1)
        else:
            seculos.add(int(ano)//100)

        if (data < ano_menor): 
            ano_menor = data
        
        elif (data > ano_maior): 
            ano_maior = data

        elif ano in anos.keys():
            anos[ano] += 1
        else:
            anos[ano] = 1
anos = dict(sorted(anos.items(), key=lambda p: p[0]))
s = '------------------------------------------------\n{:9} Número de processos por ano:\n------------------------------------------------'.format(' ')
print(s)

for i in anos:
    print(f'\t  Ano: {i}       Processos: {anos[i]}' )


s = '------------------------------------------------\n{:13} Intervalo de datas:\n------------------------------------------------'.format(' ')
print(f'{s}\n \t\t   {ano_menor}\n \t\t      até\n \t\t   {ano_maior}')

seculos = sorted(seculos)
s = '------------------------------------------------\n{:13} Séculos analisados:\n------------------------------------------------'.format(' ')
print(f'{s}\n\t   ', end='')
for s in seculos:
    print(int_to_Roman(s), end=' ; ')
print('\n')
