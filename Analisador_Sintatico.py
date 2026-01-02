import ply.yacc as yacc
from Analisador_Lexico import tokens  # importa os tokens do analisador léxico

# Programa 
def p_program(p):
    '''program : expr_list'''
    p[0] = ("program", p[1])

def p_expr_list(p):
    '''expr_list : expr expr_list
                 | expr'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

# Expressões possíveis
def p_expr(p):
    '''expr : atom
            | func_def
            | cond_expr
            | print_expr
            | read_expr
            | cons_expr
            | car_expr
            | cdr_expr
            | binop_expr
            | func_call'''   
    p[0] = p[1]

# chamadas de função genéricas
def p_func_call(p):
    '''func_call : DELIM_E ID expr_list DELIM_D
                 | DELIM_E ID DELIM_D'''
    if len(p) == 5:
        p[0] = ("call", p[2], p[3])
    else:
        p[0] = ("call", p[2], [])

# Definição de função
def p_func_def(p):
    '''func_def : DELIM_E DEFUN ID DELIM_E param_list DELIM_D expr_list DELIM_D'''
    p[0] = ("defun", p[3], p[5], p[7])

def p_param_list(p):
    '''param_list : ID param_list
                  | ID
                  | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

# Condicional
def p_cond_expr(p):
    '''cond_expr : DELIM_E IF expr expr expr DELIM_D'''
    p[0] = ("if", p[3], p[4], p[5])

# Print
def p_print_expr(p):
    '''print_expr : DELIM_E PRINT expr DELIM_D'''
    p[0] = ("print", p[3])

# Read
def p_read_expr(p):
    '''read_expr : DELIM_E READ DELIM_D'''
    p[0] = ("read",)

# Cons
def p_cons_expr(p):
    '''cons_expr : DELIM_E CONS expr expr DELIM_D'''
    p[0] = ("cons", p[3], p[4])

# Car
def p_car_expr(p):
    '''car_expr : DELIM_E CAR expr DELIM_D'''
    p[0] = ("car", p[3])

# Cdr
def p_cdr_expr(p):
    '''cdr_expr : DELIM_E CDR expr DELIM_D'''
    p[0] = ("cdr", p[3])

# Operações
def p_binop_expr(p):
    '''binop_expr : DELIM_E SOMA expr expr DELIM_D
                  | DELIM_E SUB expr expr DELIM_D
                  | DELIM_E MULTI expr expr DELIM_D
                  | DELIM_E DIVIS expr expr DELIM_D
                  | DELIM_E DIV expr expr DELIM_D
                  | DELIM_E MOD expr expr DELIM_D
                  | DELIM_E EXP expr expr DELIM_D
                  | DELIM_E LT expr expr DELIM_D
                  | DELIM_E GT expr expr DELIM_D
                  | DELIM_E EQ expr expr DELIM_D
                  | DELIM_E LE expr expr DELIM_D
                  | DELIM_E GE expr expr DELIM_D
                  | DELIM_E NE expr expr DELIM_D'''
    p[0] = ("binop", p[2], p[3], p[4])

# Átomos
def p_atom(p):
    '''atom : NUMBER
            | STRING
            | ID
            | NIL'''
    p[0] = ("atom", p[1])

# Expressão vazia
def p_empty(p):
    '''empty :'''
    p[0] = None

# Erro sintático
def p_error(p):
    if p:
        print(f"Erro sintático próximo de '{p.value}'")
    else:
        print("Erro sintático no final do código")


# Construção do parser
parser = yacc.yacc()
