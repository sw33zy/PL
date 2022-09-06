import re

f = open('processos.xml')

irmao = 0
tio = 0
primo = 0
obsline = ''
parentes = ''
candidatos = 0


def contaParentes(string):
    if res := re.findall(r'([a-zA-Z ,]+)\,([a-zA-Z ]+)\.(\ ?)([Pp][Rr][Oo][Cc])', string): 
        global irmao
        global tio
        global primo
        global candidatos
        candidatos +=1
        for p in res:
            
            if re.search(r'Irmaos', p[1]):
                irmao += len(re.findall(r'( e |,)', p[0])) + 1
            elif re.search(r'Irmao', p[1]):
                irmao +=1
            elif re.search(r'Tios', p[1]):
                tio += len(re.findall(r'( e |,)', p[0])) + 1
            elif re.search(r'Tio', p[1]):
                tio +=1
            elif re.search(r'Primos', p[1]):
                primo += len(re.findall(r'( e |,)', p[0])) + 1
            elif re.search(r'Primo', p[1]):
                primo +=1
                
                


for line in f:

    if res := re.search(r'<obs>([^<]*)(<\/obs>)?', line):
        
        if re.search(r'<\/obs>$', res.group(0)):
            contaParentes(res.group(1)) 
              
        else:
            obsline = obsline + res.group(1).strip('\n')
    elif res := re.search(r'(.*)</obs>$', line):
        obsline = obsline + ' ' + res.group(1).strip()
        contaParentes(obsline)
        obsline = ''
    elif res:= re.search(r'^[^<](.*)[^>]$',line.strip()):
        obsline = obsline + ' ' + res.group(0).strip()


s = '------------------------------------------------------\nNº de candidatos que têm parentes eclesiásticos: {:}\n------------------------------------------------------\n'.format(candidatos)
print(s)

pdict = {'Irmãos':irmao, 'Tios': tio, 'Primos': primo}
pdict = dict(sorted(pdict.items(), key=lambda p: p[1], reverse=True))
print('\t       +----------+-----------+')
for d in pdict:
    print(f'\t       |{d:10}| {pdict[d]:8}  |')
    print('\t       +----------+-----------+')


s = '\n------------------------------------------------------\n      Tipo de parentesco mais frequente: {:6}\n------------------------------------------------------\n'.format(list(pdict.keys())[0])
print(s)