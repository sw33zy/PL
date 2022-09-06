import sys
import ply.yacc as yacc
from tp2_lex import tokens
import re

error = 0
condCounter = 0
condStack = []
errorCounter = 0

output = ""

# -----------------------------------------------------------------------------
# Prog ------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Prog(p):
    "Prog : InitBlock"


def p_Prog_Complete(p):
    "Prog : InstrBlock"

# -----------------------------------------------------------------------------
# InitBlock ------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_InitBlock_Single(p):
    "InitBlock : Init"


def p_InitBlock_List(p):
    "InitBlock : InitBlock Init"

# -----------------------------------------------------------------------------
# Init ------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Init_Int(p):
    "Init : INTID VAR"
    global output, errorCounter
    if (p.parser.register.get(p[2]) == None):
        output += ("pushi 0\n")
        p.parser.register.update({p[2]: (p.parser.counter, 1, 1)})
        p.parser.counter += 1
    else:
        output += ("err \"variable '" + p[2] + "' already exists\"\n")
        errorCounter += 1


def p_Init_Array(p):
    "Init : INTID '[' INT ']' VAR"
    global output, errorCounter
    if (p.parser.register.get(p[5]) == None):
        output += ("pushn " + p[3] + "\n")
        p.parser.register.update({p[5]: (p.parser.counter, int(p[3]), 1)})
        p.parser.counter += int(p[3])
    else:
        output += ("err \"variable '" + p[5] + "' already exists\"\n")
        errorCounter += 1


def p_Init_Matrix(p):
    "Init : INTID '[' INT ']' '[' INT ']' VAR"
    global output, errorCounter
    if (p.parser.register.get(p[8]) == None):
        output += ("pushn " + str(int(p[3])*int(p[6])) + "\n")
        p.parser.register.update(
            {p[8]: (p.parser.counter, int(p[3]), int(p[6]))})
        p.parser.counter += int(p[3]) * int(p[6])
    else:
        output += ("err \"variable '" + p[8] + "' already exists\"\n")
        errorCounter += 1

# -----------------------------------------------------------------------------
# InstrBlock ------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_InstrBlock_Single(p):
    "InstrBlock : Command"


def p_InstrBlock_List(p):
    "InstrBlock : InstrBlock Command"

# -----------------------------------------------------------------------------
# Command ---------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Command_Atrib(p):
    "Command : Atrib"


def p_Command_Read(p):
    "Command : Read"


def p_Command_Write(p):
    "Command : Write"


def p_Command_IfStatement(p):
    "Command : IfStatement"


def p_Command_ForStatement(p):
    "Command : ForStatement"

# -----------------------------------------------------------------------------
# Atrib -----------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Atrib_Expr(p):
    "Atrib : VAR '=' Expr"
    global output, errorCounter
    if(p.parser.register.get(p[1]) == None):
        output += ("err \"variable '" + p[1] + "' does not exist\"\n")
        errorCounter += 1
    elif (error != 1):
        output += ("storeg " + str(p.parser.register.get(p[1])[0]) + "\n")


def p_Atrib_Read(p):
    "Atrib : VAR  '=' Read"
    global output, errorCounter
    if(p.parser.register.get(p[1]) == None):
        output += ("err \"variable '" + p[1] + "' does not exist\"\n")
        errorCounter += 1
    elif (error != 1):
        output += ("atoi \n")
        output += ("storeg " + str(p.parser.register.get(p[1])[0]) + "\n")


def p_Atrib_Array_Int(p):
    "Atrib : VAR '[' INT ']' '=' Expr"
    global output, errorCounter
    if(p.parser.register.get(p[1]) == None):
        output += ("err \"variable '" + p[1] + "' does not exist\"\n")
        errorCounter += 1
    elif (int(p[3]) >= p.parser.register.get(p[1])[1]):
        output += ("err \" Segmentation fault! variable '" + p[1] + "' \"\n")
        errorCounter += 1
    elif (error != 1):
        output += ("storeg " +
                   str(p.parser.register.get(p[1])[0] + int(p[3])) + "\n")


def p_Atrib_Array_Var(p):
    "Atrib : AtribArray '=' Expr"
    global output
    output += ("storen\n")


def p_AtribArray(p):
    "AtribArray : VAR '[' VAR ']'"
    global output, errorCounter
    if(p.parser.register.get(p[1]) == None):
        output += ("err \"variable '" + p[1] + "' does not exist\"\n")
        errorCounter += 1
    elif (error != 1):
        output += ("pushgp\n")
        output += ("pushi " + str(p.parser.register.get(p[1])[0]) + "\n")
        output += ("pushg " + str(p.parser.register.get(p[3])[0]) + "\n")
        output += ("add\n")


def p_Atrib_Array_Read_Int(p):
    "Atrib :  VAR '[' INT ']' '=' Read"
    global output, errorCounter
    if(p.parser.register.get(p[1]) == None):
        output += ("err \"variable '" + p[1] + "' does not exist\"\n")
        errorCounter += 1
    elif (int(p[3]) >= p.parser.register.get(p[1])[1]):
        output += ("err \" Segmentation fault! variable '" + p[1] + "' \"\n")
        errorCounter += 1
    elif (error != 1):
        output += ("atoi \n")
        output += ("storeg " +
                   str(p.parser.register.get(p[1])[0] + int(p[3])) + "\n")


def p_Atrib_Array_Read_Var(p):
    "Atrib :  AtribArray '=' Read"
    global output, errorCounter
    if (error != 1):
        output += ("atoi \n")
        output += ("storen\n")


def p_Atrib_Matrix_Int(p):
    "Atrib : VAR '[' INT ']' '[' INT ']' '=' Expr"
    global output, errorCounter
    var = p.parser.register.get(p[1])
    if(p.parser.register.get(p[1]) == None):
        output += ("err \"variable '" + p[1] + "' does not exist\"\n")
        errorCounter += 1
    elif (int(p[3]) >= var[1] or int(p[6]) >= var[2]):
        output += ("err \" Segmentation fault! variable '" + p[1] + "' \"\n")
        errorCounter += 1
    elif (error != 1):
        output += ("storeg " + str(var[0] + var[2] * int(p[3]) + (int(p[6]))) + "\n")


def p_Atrib_Matrix_Read_Int(p):
    "Atrib : VAR '[' INT ']' '[' INT ']' '=' Read"
    global output, errorCounter
    var = p.parser.register.get(p[1])
    if(p.parser.register.get(p[1]) == None):
        output += ("err \"variable '" + p[1] + "' does not exist\"\n")
        errorCounter += 1
    elif (int(p[3]) >= var[1] or int(p[6]) >= var[2]):
        output += ("err \" Segmentation fault! variable '" + p[1] + "' \"\n")
        errorCounter += 1
    elif (error != 1):
        output += ("atoi \n")
        output += ("storeg " + str(var[0] + var[2] * int(p[3]) + (int(p[6]))) + "\n")

def p_AtribMatrix(p):
    "AtribMatrix : VAR '[' VAR ']' '[' VAR ']'"
    global output, errorCounter
    if(p.parser.register.get(p[1]) == None):
        output += ("err \"variable '" + p[1] + "' does not exist\"\n")
        errorCounter += 1
    elif (error != 1):
        output += ("pushgp\n")
        output += ("pushi " + str(p.parser.register.get(p[1])[0]) + "\n")
        output += ("pushi " + str(p.parser.register.get(p[1])[2]) + "\n")
        output += ("pushg " + str(p.parser.register.get(p[3])[0]) + "\n")
        output += ("mul\n")
        output += ("pushg " + str(p.parser.register.get(p[6])[0]) + "\n")
        output += ("add\n")
        output += ("add\n")

def p_Atrib_Matrix_Var(p):
    "Atrib : AtribMatrix '=' Expr"
    global output
    output += ("storen\n")

def p_Atrib_Matrix_Read_Var(p):
    "Atrib :  AtribMatrix '=' Read"
    global output, errorCounter
    if (error != 1):
        output += ("atoi \n")
        output += ("storen\n")

# -----------------------------------------------------------------------------
# Read ------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Read(p):
    "Read : READ '(' ')'"
    global output
    output += ("read \n")

# -----------------------------------------------------------------------------
# Write -----------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Write_String(p):
    "Write : WRITE '(' STRING ')'"
    global output
    output += ("pushs " + p[3] + "\n")
    output += ("writes \n")


def p_Write_Var(p):
    "Write : WRITE '(' VAR ')'"
    global output
    output += ("pushg " + str(p.parser.register.get(p[3])[0]) + "\n")
    output += ("stri\n")
    output += ("writes\n")


def p_Write_Array_Int(p):
    "Write : WRITE '(' VAR '[' INT ']' ')'"
    global output
    output += ("pushg " +
               str(p.parser.register.get(p[3])[0] + int(p[5])) + "\n")
    output += ("stri\n")
    output += ("writes\n")


def p_Write_Array_Var(p):
    "Write : WRITE '(' AtribArray ')'"
    global output
    output += ("loadn\n")
    output += ("stri\n")
    output += ("writes\n")

def p_Write_Matrix_Int(p):
    "Write : WRITE '(' VAR '[' INT ']' '[' INT ']' ')'"
    var = p.parser.register.get(p[1])
    global output
    output += ("pushg " + str(var[0] + var[2] * int(p[3]) + (int(p[6]))) + "\n")
    output += ("stri\n")
    output += ("writes\n")


def p_Write_Matrix_Var(p):
    "Write : WRITE '(' AtribMatrix ')'"
    global output
    output += ("loadn\n")
    output += ("stri\n")
    output += ("writes\n")
    
# -----------------------------------------------------------------------------
# IfStatement -----------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_IfStatement(p):
    "IfStatement : If '{' Body '}'"
    global output
    output += ("endif" + str(condStack.pop()) + ":" + "\n")

# -----------------------------------------------------------------------------
# If --------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_If(p):
    "If : IFID '(' Cond ')'"
    global condCounter, condStack, output
    condStack.append(condCounter)
    output += ("jz endif" + str(condCounter) + "\n")
    condCounter += 1

# -----------------------------------------------------------------------------
#  Body -----------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Body_Single(p):
    "Body : Command"


def p_Body_List(p):
    "Body : Body Command"

# -----------------------------------------------------------------------------
# ForStatement ----------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_ForStatement(p):
    "ForStatement : For '{' Body '}'"
    global output
    output += ("jump repeat" + str(condStack[(len(condStack)-1)]) + "\n")
    output += ("repeatend" + str(condStack.pop()) + ":\n")

# -----------------------------------------------------------------------------
# For -------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_For(p):
    "For : FORID '(' Atrib InitLabel ForCond ')'"

# -----------------------------------------------------------------------------
# InitLabel -------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_InitLabel(p):
    "InitLabel : ';'"
    global condCounter, condStack, output
    condStack.append(condCounter)
    output += ("repeat" + str(condCounter) + ":\n")
    condCounter += 1

# -----------------------------------------------------------------------------
# ForCond ---------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_ForCond(p):
    "ForCond : Cond"
    global output
    output += ("jz repeatend" + str(condStack[(len(condStack)-1)]) + "\n")

# -----------------------------------------------------------------------------
# Cond ------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Cond_Equals(p):
    "Cond : Factor '=' '=' Factor"
    global output
    output += ("equal\n")


def p_Cond_NotEquals(p):
    "Cond : Factor '!' '=' Factor"
    global output
    output += ("equal\nnot\n")


def p_Cond_Greater(p):
    "Cond : Factor '>' Factor"
    global output
    output += ("sup\n")


def p_Cond_GreaterEquals(p):
    "Cond : Factor '>' '=' Factor"
    global output
    output += ("supeq\n")


def p_Cond_MinorEquals(p):
    "Cond : Factor '<' '=' Factor"
    global output
    output += ("infeq\n")


def p_Cond_Minor(p):
    "Cond : Factor '<' Factor "
    global output
    output += ("inf\n")

# -----------------------------------------------------------------------------
# Expr ------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Expr_add(p):
    "Expr : Expr '+' Term"
    global output
    if (error != 1):
        output += ("add\n")


def p_Expr_sub(p):
    "Expr : Expr '-' Term"
    global output
    if (error != 1):
        output += ("sub\n")


def p_Expr_Term(p):
    "Expr : Term"

# -----------------------------------------------------------------------------
# Term ------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Term_mull(p):
    "Term : Term '*' Factor"
    global output
    if (error != 1):
        output += ("mul\n")


def p_Term_div(p):
    "Term : Term '/' Factor"
    global output
    if (error != 1):
        output += ("div\n")


def p_Term_mod(p):
    "Term : Term '%' Factor"
    global output
    if (error != 1):
        output += ("mod\n")


def p_Term_Factor(p):
    "Term : Factor"

# -----------------------------------------------------------------------------
# Factor ----------------------------------------------------------------------
# -----------------------------------------------------------------------------

def p_Factor_INT(p):
    "Factor : INT"
    global output
    if (error != 1):
        output += ("pushi "+p[1]+"\n")


def p_Factor_VAR(p):
    "Factor : VAR"
    global output, errorCounter, error
    if(p.parser.register.get(p[1]) == None):
        error = 1
        output += ("err \"variable '" + p[1] + "' is not defined\"\n")
        errorCounter += 1
    elif (p.parser.register.get(p[1])[1] > 1):
        error = 1
        output += ("err \"Unsupported operand type(s)\"\n")
        errorCounter += 1
    else:
        output += ("pushg " + str(p.parser.register.get(p[1])[0]) + "\n")


def p_Factor_VAR_Int(p):
    "Factor : VAR '[' INT ']'"
    global output, errorCounter, error
    if(p.parser.register.get(p[1]) == None):
        error = 1
        output += ("err \"variable '" + p[1] + "' is not defined\"\n")
        errorCounter += 1
    elif(p.parser.register.get(p[1])[1] == 1):
        error = 1
        output += ("err \"'int' object is not subscriptable\"\n")
        errorCounter += 1
    else:
        output += ("pushg " +
                   str(p.parser.register.get(p[1])[0] + int(p[3])) + "\n")


def p_Factor_VAR_Int_Int(p):
    "Factor : VAR '[' INT ']' '[' INT ']'"
    global output, errorCounter, error
    var = p.parser.register.get(p[1])
    if(p.parser.register.get(p[1]) == None):
        error = 1
        output += ("err \"variable '" + p[1] + "' is not defined\"\n")
        errorCounter += 1
    elif(p.parser.register.get(p[1])[1] == 1):
        error = 1
        output += ("err \"'int' object is not subscriptable\"\n")
        errorCounter += 1
    else:
        output += ("pushg " + str(var[0] + var[2] * int(p[3]) + (int(p[6]))) + "\n")


def p_Factor_group(p):
    "Factor : '(' Expr ')'"


def p_error(p):
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


parser = yacc.yacc()

parser.register = {}

parser.counter = 0
inFile = open("test.txt")

codeBlock = False
aux = ""
chavetas = 0

for linha in inFile:
    error = 0

    if ("{") in linha:
        codeBlock = True
        chavetas += 1

    if ("}") in linha:
        codeBlock = False
        chavetas -= 1

    aux += linha

    if chavetas == 0:
        result = parser.parse(aux)
        aux = ""

inFile.close()

print(parser.register)
outFile = open("output.txt", "w", encoding="ascii")

if(errorCounter > 0):
    errors = re.findall(r'err \"[^\"]+\"[ ]*\n', output)
    output = ''.join(errors)

outFile.write(output)
outFile.close()
