# Compilador

Aqui estão os trabalhos desenvolvidos para a disciplina de compiladores (CI211)
do curso de Ciência da Computação da Universidade Federal do Paraná.

Alunos: Alexandre Calerio de Oliveira e Felipe Mariani Lopes

## Analisador Léxico
O diretório [analisador_lexico](analisador_lexico/) centraliza todos os arquivos
desenvolvidos no primeiro trabalho da disciplina, lá pode ser encontrada a documentação
do projeto, o diagrama de estados do autômato do analisador léxico e a descrição da
gramática até aquele ponto, na perspectiva léxica.

## Analisador Sintático
O diretório [analisador_sintatico](analisador_sintatico/) contém o analisador sintático
slr desenvolvido e a documentação apresentando as decisões de projeto.

## Execução
Os dois módulos (analisador_lexico e analisador_sintatico) podem ser utilizados
independentemente, sendo incluídos em outros projetos. Entretanto, para facilitar
os testes, foi criado o arquivo compiler.py que congrega os dois módulos e implementa
o esquema de compilação usando a análise léxica e a análise sintática.

A execução do código é bem simples:

```bash
$ python compiler.py testes/simples.c
```

O comando acima irá rodar o compilador passando como entrada o arquivo de testes
simples.c.

