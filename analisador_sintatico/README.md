#Analisador Léxico

##Definição do trabalho 2
Fazer o analisador sintático SLR(1) para a linguagem definida em sala.

###Entregar 
* Tabela de análise sintática SLR(1)
* Relatório (este arquivo)
* Data: 21/06/16
* Em dupla
* Valor: 3.0

##Mudanças na gramática
Na gramática definida em classe existiam algumas regras que tratavam dos tokens de números,
são elas:

NUM -> NUM_INT | NUM_FLOAT

NUM_INT -> DIGITO NUM_INT | DIGITO

NUM_FLOAT -> NUM_INT.NUM_INT

Estas regras saíram da gramática do nosso trabalho pois a análise léxica já resolve o problema
com os diferentes tipos de números, retornando um token num, contendo o número encontrado,
independente de ser inteiro ou float, respeitando, em ambos os casos, as regras de formação
de inteiros e float da linguagem definida.

