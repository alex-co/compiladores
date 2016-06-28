# Compilador

Aqui estão os trabalhos desenvolvidos para a disciplina de compiladores (CI211)
do curso de Ciência da Computação da Universidade Federal do Paraná.

Alunos: Alexandre Calerio de Oliveira e Felipe Mariani Lopes

## Trabalho 1: Analisador Léxico
O diretório [analisador_lexico](analisador_lexico/) centraliza todos os arquivos
desenvolvidos no primeiro trabalho da disciplina, lá pode ser encontrada a documentação
do projeto, o diagrama de estados do autômato do analisador léxico e a descrição da
gramática até aquele ponto, na perspectiva léxica.

## Trabalho 2: Analisador Sintático
O diretório [analisador_sintatico](analisador_sintatico/) contém o analisador sintático
slr desenvolvido e a documentação apresentando as decisões de projeto.

## Trabalho 3: Verificador de Tipos
O diretório [verificador_tipos](verificador_tipos/) contém arquivo veritypes.py que
por sua vez contém a classe que faz a verificação de tipos do código fonte C simplificado.

## Execução
Os do analisador_lexico e analisador_sintatico podem ser utilizados independentemente,
sendo incluídos em outros projetos. No entanto a verificação de tipos é dependente dos
analisadores. Para facilitar os testes, foi criado o arquivo compiler.py que congrega 
os três módulos e implementa o esquema de compilação usando a análise léxica, a análise sintática
juntamente com a verificação de tipos.

A execução do código é bem simples:

```bash
$ python compiler.py testes/simples.c
```

O comando acima irá rodar o compilador passando como entrada o arquivo de testes
simples.c.

