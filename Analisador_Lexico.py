import ply.lex as lex

# Lista de tokens
tokens = [
    'SOMA', 'SUB', 'MULTI', 'DIVIS', 'DIV', 'MOD', 'EXP',
    'LT', 'GT', 'EQ', 'LE', 'GE', 'NE',
    'DEFUN', 'IF', 'PRINT', 'READ',
    'CAR', 'CDR', 'CONS', 'NIL',
    'NUMBER', 'STRING',
    'DELIM_E', 'DELIM_D',
    'ID'
]

# Regras dos tokens (operadores)
t_SOMA      = r'\+'
t_SUB       = r'-'
t_MULTI     = r'\*'
t_DIVIS     = r'/'
t_DIV       = r'div'
t_MOD       = r'mod'
t_EXP       = r'exp'
t_LT        = r'<'
t_GT        = r'>'
t_EQ        = r'='
t_LE        = r'<='
t_GE        = r'>='
t_NE        = r'(/=)|(!=)'

# Delimitadores
t_DELIM_E   = r'\('
t_DELIM_D   = r'\)'

# Strings
t_STRING    = r'\"([^\\\"]|\\.)*\"'

# Palavras reservadas
reserved = {
    'defun': 'DEFUN',
    'if': 'IF',
    'cond': 'COND',
    'print': 'PRINT',
    'read': 'READ',
    'car': 'CAR',
    'cdr': 'CDR',
    'cons': 'CONS',
    'nil': 'NIL'
}

# Identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_-]*'
    t.type = reserved.get(t.value, 'ID')  # Se estiver em reserved, vira palavra reservada
    return t

# Números
def t_NUMBER(t):
    r'[0-9]+(\.[0-9]+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Comentários (ignora até o fim da linha)
def t_COMMENT(t):
    r';.*'
    pass

# Ignorar espaços e quebras de linha
t_ignore = ' \t\r\n'

# Tratamento de erro
def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()

