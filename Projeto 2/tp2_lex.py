#Ordem de tratamento na contrução de um compilador
#
# 1. exppressões aritméticas
# 2. variáveis (escalares, arrays)
# 3. condicionais (exp. boleanas, ) 
# 4. ciclos (repeat n, while(cnd), repeat.until(cnd), for)
#
import ply.lex as lex


reserved = {
   'if' : 'IFID',
   'int' : 'INTID',
   'scan' : 'READ',
   'print' : 'WRITE',
   'for' : 'FORID'
}


tokens = ['INT', 'VAR', 'STRING', 'ID'] + list(reserved.values())
literals = ['(', ')', '+', '-', '*', '/', '=', '>', '<', '!', '{', '}', ';', '%', '[', ']']

def t_ID(t):
    r'if|int|scan|print|for'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_INT = r'(\+|-)?(\d+)'
t_VAR = r'[a-zA-Z]\w*'

t_STRING = r'"[^"]*"'


t_ignore = " \t\n\r" 

def t_error(t):
    print("Ilegal Character: ", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
