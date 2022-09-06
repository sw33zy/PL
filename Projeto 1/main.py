
s = "Bem-Vindo ao Arquivo dos Róis de Confessados!"
print(f'\n--------------------------------------------------\n  {s}\n--------------------------------------------------')

def menu():
    print("\n  > 1 - Número de processos, listagem e intervalo de datas de registos.\n\
  > 2 - Os 5 nomes e apelidos mais frequentes por século.\n\
  > 3 - Número de candidatos com parentes e a sua frequência de parentesco.\n\
  > 4 - Pais com mais do que um filho candidato.\n\
  > 5 - Árvores genealógicas dos candidatos referentes a um ano.\n\
  > 6 - Ajuda.\n\
  > 0 - Sair.\n")

menu()
opcao = input ("Insira uma opção:\n> ")

while(opcao!="0"):
    if(opcao == "1"):
        exec(open("./alineaA.py", encoding="utf-8").read())
    elif(opcao == "2"):
        exec(open("./alineaB.py", encoding="utf-8").read())
    elif(opcao == "3"):
        exec(open("./alineaC.py", encoding="utf-8").read())
    elif(opcao == "4"):
        exec(open("./alineaD.py", encoding="utf-8").read())
    elif(opcao == "5"):
        exec(open("./alineaE.py", encoding="utf-8").read())
    elif(opcao == "6"):
        menu()
    else:
        print("Opção Inválida, Tente Novamente!")
    opcao = input ("Insira uma opção:\n> ")