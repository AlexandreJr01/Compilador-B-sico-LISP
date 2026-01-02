# 🧠 Projeto Compilador Lisp

Compilador/interpretador de um **subconjunto da linguagem Lisp**, implementado em **Python**, desenvolvido como projeto acadêmico da disciplina de **Compiladores**.

---

## 😎 Descrição

Este projeto implementa as etapas fundamentais do processo de compilação, permitindo a análise e execução de programas Lisp simplificados. O sistema realiza desde a análise léxica até a execução por meio de uma máquina virtual, com suporte a funções, recursão e manipulação de listas.

Durante a execução, o compilador é capaz de:

- Analisar expressões Lisp por meio de **análise léxica e sintática**.  
- Construir uma **Árvore Sintática Abstrata (AST)**.  
- Gerar **código intermediário** no formato de três endereços.  
- Executar o código em uma **máquina virtual**.  
- Definir e chamar funções (`defun`).  
- Manipular listas (`cons`, `car`, `cdr`, `nil`).  
- Executar operações aritméticas e condicionais (`if`, `eq`).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3  
- **Biblioteca:** PLY (Python Lex-Yacc)  
- **Paradigma:** Compiladores e Interpretadores  
- **Estruturas de Dados:** Listas, Tuplas e Dicionários  

---

## 🚀 Como Executar

1. Instale a dependência necessária:
   ```bash
   pip install ply


Execute o compilador:

 ```bash
python Compilador.py
```


Um terminal interativo será iniciado.
Digite expressões Lisp ou sair para encerrar.
--- 

## 🧪 Exemplo de Uso
(defun soma (lista)
  (if (eq lista nil)
      0
      (+ (car lista) (soma (cdr lista)))))

(soma (cons 10 (cons 20 (cons 30 nil))))

## ⚠️ Limitações
Suporte apenas a um subconjunto da linguagem Lisp
Tipagem dinâmica sem verificação estática
Escopo simplificado baseado em cópia de memória
Ausência de otimizações no código intermediário

