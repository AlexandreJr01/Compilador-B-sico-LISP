from Analisador_Sintatico import parser

class Interpretador:
    def __init__(self):
        self.codigo_intermediario = []
        self.temp_count = 0

    #Função auxiliar para endereçar as instruções ou valores temporários
    def novo_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"


    # Código Intermediário para Arquivo 
    def salvar_codigo_em_arquivo(self, nome_arquivo="codigo_Intermediario.txt"):
        try:
            with open(nome_arquivo, "w") as f:
                f.write("=== Código Intermediário ===\n")
                for i, instr in enumerate(self.codigo_intermediario):
                    f.write(f"{i}: {str(instr)}\n")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")


    # Gerador de código Intermediário
    def gerar_ci(self, no):
        #Evita a arvore de derivação com incompleta(erro)
        if no is None: return None
        if not isinstance(no, (tuple, list)): return no #Garante que não vai ter loop inifinito
        #Se for uma lista, vai gerar o código recursivamente
        if isinstance(no, list):
            res = None
            for elem in no:
                res = self.gerar_ci(elem)
            return res
        
        #Pega o token no inicio da tupla
        tipo = no[0]

        # Program
        if tipo == "program":
            return self.gerar_ci(no[1])
        #Atom
        elif tipo == "atom":
            valor = no[1]
            if valor == "nil": valor = "nil"
            #Valor solto 
            self.codigo_intermediario.append(("atom", valor, None, None))
            return valor
        #Binop 
        elif tipo == "binop":
            op = no[1]
            arg1 = self.gerar_ci(no[2])
            arg2 = self.gerar_ci(no[3])
            t = self.novo_temp() #Endereçando
            self.codigo_intermediario.append((op, arg1, arg2, t))
            return t

        #Cons
        elif tipo == "cons":
            arg1 = self.gerar_ci(no[1])
            arg2 = self.gerar_ci(no[2])
            t = self.novo_temp() #Endereçando
            self.codigo_intermediario.append(("cons", arg1, arg2, t))
            return t
        #Car e Cdr 
        elif tipo in ("car", "cdr"):
            arg1 = self.gerar_ci(no[1])
            t = self.novo_temp() #Endereçando
            self.codigo_intermediario.append((tipo, arg1, None, t))
            return t
        #Print
        elif tipo == "print":
            arg1 = self.gerar_ci(no[1])
            self.codigo_intermediario.append(("print", arg1, None, None))
            return arg1

        #If
        elif tipo == "if":
            #Gera o código temporário da condição
            cond = self.gerar_ci(no[1])
            
            #Guarda o código para não misturar
            backup = self.codigo_intermediario.copy()

            #Gera o código se a condição for verdadeira
            self.codigo_intermediario.clear()
            self.gerar_ci(no[2])
            bloco_true = self.codigo_intermediario.copy()

            #Gera o código se a condição for falsa
            self.codigo_intermediario.clear()
            self.gerar_ci(no[3])
            bloco_false = self.codigo_intermediario.copy()

            #Trás o código devolta
            self.codigo_intermediario.clear()
            self.codigo_intermediario.extend(backup)
            
            t = self.novo_temp() #Endereçando
            self.codigo_intermediario.append(("if", cond, bloco_true, bloco_false, t))
            return t

        #Call
        elif tipo == "call":
            #Nome e argumento da função
            nome_func = no[1]
            args_func = no[2]

            
            if nome_func == "eq":
                a1 = self.gerar_ci(args_func[0])
                a2 = self.gerar_ci(args_func[1])
                t = self.novo_temp() #Endereçando
                self.codigo_intermediario.append(("eq", a1, a2, t))
                return t
            #Gera o código dos argumentos da função
            args_vals = [self.gerar_ci(arg) for arg in args_func]
            t = self.novo_temp()
            self.codigo_intermediario.append(("call", nome_func, args_vals, t))
            return t

        #Defun
        elif tipo == "defun":
            #Nome, parametro e corpo da função
            nome = no[1]
            params = no[2]
            corpo_arv = no[3]
            #Guarda o códígo para não misturar
            backup = self.codigo_intermediario.copy()
            self.codigo_intermediario.clear()

            #Gera o código do corpo e coloca na memória
            self.gerar_ci(corpo_arv)
            corpo_ci = self.codigo_intermediario.copy()

            self.codigo_intermediario.clear()
            self.codigo_intermediario.extend(backup)

            self.codigo_intermediario.append(("defun", nome, params, corpo_ci))
            return nome


#Maquina Virtual
class Compilador:
    def __init__(self):
        self.memoria = {}
        self.funcoes = {}

    # Execução do código
    def executar(self, ci):
        retorno_exe = None

        for instr in ci:
            # Pega o operador pelo índice 0
            op = instr[0]
            #Atom
            if op == "atom":
                val = instr[1]
                retorno_exe = self.memoria.get(val, val)
            #If
            elif op == "if":
                cond = instr[1]
                b_true = instr[2]
                b_false = instr[3]
                r = instr[4]
                #Pega o valor temporário ou direto através do endereço
                val = self.memoria.get(cond, cond)
                #Se a Condição é verdadeira
                if val != "nil" and val is not False and val is not None:
                    retorno_exe = self.executar(b_true)
                else:
                #Se a condição é falsa
                    retorno_exe = self.executar(b_false)
                self.memoria[r] = retorno_exe

            #Defun
            elif op == "defun":
                
                nome = instr[1]
                params = instr[2]
                corpo = instr[3]
                #Guarda na lista de funções definidas
                self.funcoes[nome] = (params, corpo)
                retorno_exe = nome

            #Call
            elif op == "call":
                # Acesso por índices: (call, nome, args, result)
                nome_func = instr[1]
                args_temporarios = instr[2]
                r = instr[3]
                
                if nome_func in self.funcoes:
                    #Busca dados da função
                    dados_funcao = self.funcoes[nome_func]
                    f_params = dados_funcao[0]
                    f_corpo = dados_funcao[1]

                    #Procura o valor dos argumentos
                    vals_args = [self.memoria.get(arg, arg) for arg in args_temporarios]
                    
                    #Backup da memória antes da execução do compo da função
                    mem_backup = self.memoria.copy()
                    
                    #Sincroniza os valores dos parametros
                    for p, val in zip(f_params, vals_args):
                        self.memoria[p] = val
                        
                    #Executa
                    retorno = self.executar(f_corpo)
                    
                    # Restaura a memória
                    self.memoria = mem_backup
                    
                    # Salva o resultado da função
                    self.memoria[r] = retorno
                    retorno_exe = retorno
                else:
                    print(f"ERRO: Função '{nome_func}' não definida.")
                    return None
            #Print
            elif op == "print":
                val = instr[1]
                print(self.memoria.get(val, val))
                retorno_exe = None

            #Operações
            else:
                a = instr[1]
                b = instr[2]
                r = instr[3]

                v1 = self.memoria.get(a, a)
                v2 = self.memoria.get(b, b)

                #Aritmética
                if op == '+': self.memoria[r] = v1 + v2; retorno_exe = self.memoria[r]
                elif op == '-': self.memoria[r] = v1 - v2; retorno_exe = self.memoria[r]
                elif op == '*': self.memoria[r] = v1 * v2; retorno_exe = self.memoria[r]
                elif op == '/': self.memoria[r] = v1 / v2; retorno_exe = self.memoria[r]
                
                #Comparação
                elif op == "eq":
                    self.memoria[r] = (v1 == v2)
                    retorno_exe = self.memoria[r]

                #Listas
                elif op == "cons":
                    cabeca = v1
                    cauda = v2
                    if cauda == "nil" or cauda is None: cauda = []
                    elif not isinstance(cauda, list): cauda = [cauda]
                    self.memoria[r] = [cabeca] + cauda
                    retorno_exe = self.memoria[r]

                elif op == "car":
                    lista = v1
                    if isinstance(lista, list) and len(lista) > 0:
                        self.memoria[r] = lista[0]
                    else: self.memoria[r] = "nil"
                    retorno_exe = self.memoria[r]

                elif op == "cdr":
                    lista = v1
                    if isinstance(lista, list) and len(lista) > 0:
                        nova = lista[1:]
                        self.memoria[r] = nova if len(nova) > 0 else "nil"
                    else: self.memoria[r] = "nil"
                    retorno_exe = self.memoria[r]

        return retorno_exe


# Terminal
def terminal():
    print(">>> Terminal <<<")
    
    vm = Compilador()

    while True:
        try:
            entrada = input(">>> ")
            if entrada.lower() == "sair": break
            if not entrada.strip(): continue

            arv_derivada = parser.parse(entrada)
            if arv_derivada is None: continue

            compilador = Interpretador()
            
            compilador.gerar_ci(arv_derivada)
            compilador.salvar_codigo_em_arquivo("codigo_gerado.txt")
            
            ci = compilador.codigo_intermediario

            if isinstance(arv_derivada, tuple) and arv_derivada[0] == "defun":
                vm.executar(ci)
                print(f"Função '{arv_derivada[1]}' definida.")
            else:
                res = vm.executar(ci)
                if res is not None:
                    if res == "nil": print("nil")
                    else: print(res)

        except Exception as e:
            #Aponta o Erro
            print("Erro:", e)

if __name__ == "__main__":
    terminal()