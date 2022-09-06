import re

f = open('processos.xml')

casal = {}
pai = ''
mae = ''
for line in f:

    if resPai := re.search(r'<pai>((.|\n)*)<\/pai>',line) :
        pai = resPai.group(1)
    if resMae := re.search(r'<mae>((.|\n)*)<\/mae>',line) :
        mae = resMae.group(1)
    
        if (pai,mae) in casal.keys():
            casal[pai,mae] += 1
        else:
            casal[pai,mae] = 1

casal = {key:val for key, val in casal.items() if int(val) != 1}
casal = dict(sorted(casal.items(), key=lambda p: p[1]))

for c in casal:
    print(f'+--------------------------------------------------------\n| Pai: {c[0]}\n| Mãe: {c[1]}\n| Nº de filhos: {casal[c]}\n+--------------------------------------------------------')


