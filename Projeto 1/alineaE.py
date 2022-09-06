from graphviz import Digraph
import re
import os
import shutil
try:
    shutil.rmtree("árvores")
except OSError as e:
    pass

ano = input ("Insira um ano:\n> ")
opcao = input("\nGerar um único ficheiro    (1)\nGerar múltiplos ficheiros  (2)\n> ")
print('A gerar ficheiros....')

cont1 = 0
cont2 = 0
f = open('processos.xml')
familia = []
mae = ''
pai = ''
filho = ''
for line in f:
    if res := re.search(r'<data>('+ano+').*<\/data>', line) :
        year = re.split(r'-', res.group(1))[0]
        cont1 += 1

    if res2 := re.search(r'<nome>(.*)<\/nome>', line) :
        if (cont2 < cont1) :
            filho = res2.group(1)

    if res3 := re.search(r'<pai>(.*)<\/pai>', line) :
        if (cont2 < cont1) :
            pai = res3.group(1)

    if res4 := re.search(r'<mae>(.*)<\/mae>', line) :
        if (cont2 < cont1) :
            mae = res4.group(1)
            familia.append((filho,pai,mae))
            cont2 +=1


def opcao_sep(familia):
    i = 0
    for f in familia:
        aux = str(i)
        aux = Digraph(comment='Árvore genealógica')

        aux.node('1', f[0])
        aux.node('2', f[1])
        aux.node('3', f[2])

        aux.edges(['21','31'])
        

        aux.render('árvores/'+str(i)+'.gv')
        i+=1

def opcao_junta(familia):
    i=0
    dot = Digraph(comment='Árvore genealógica')
    for f in familia:
        aux = str(i)
        str0 = "a"+aux
        str1 = "b"+aux
        str2 = "c"+aux
        dot.node(str0, f[0])
        dot.node(str1, f[1])
        dot.node(str2, f[2])

        dot.edge(str1,str0, constraint='true')
        dot.edge(str2,str0, constraint='true')
        i+=1

    dot.render('árvores/árvores.gv') 

if(opcao == '1'): 
    opcao_junta(familia)
else:
    opcao_sep(familia)

if len(familia)==0:
    print('\nNão há nenhuma ocorrência do ano inserido!')
else:
    print('\nFicheiros Gerados!')