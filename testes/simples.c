
/*
const int UM = 1
*/

/*
int functionc() {
    int d;
    d = 2;
    return d;
}
*/

main {

/* === Testes para atribuições: === */

    /* TESTE: atribuição para constante */
    /* "abc" = 3; */

    /* TESTE: 'y' não foi declarado */
    /*
    y = 12;
    */

    /* TESTE: Atribuição de tipos diferentes */
    /*
    int   e;
    char  c;
    float f;
    c = 'a';
    e = c;
    i = 22;
    */
    /*
    string s;
    s = "xyz";
    */
/* === Testes para operações matemáticas: === */

    int i;
    int j;
    int k;

    char c;
    char d;

    float g;
    float h;

    string m;
    string n;
    string o;

    /* Operador aritmético em um tipo não numérico */
    /* m = n * o; */
    k = 3 * 12;
    k = 10 / j;
    /* k = 9 % 3; => ERRO no analisador sintático <= */

    /* Operador de ponto flutuante aplicado a inteiro */
    /* i = j # k; */
    g = h # 3.14;

    /* Operador de inteiro aplicado a ponto flutuante */
    /* g = h / 1.18; */
    i = j / k;

    /* Incremento aplicado a ponto flutuante */
    /* g++; */

    /* Decremento aplicado a string */
    /* m--; */

    j = 2; j--;
    k = i + j;

    if( i >= 3 && j < 10 ) {
        k = j + 1;
    }

    for( i = 0; i <= j; i++ ) {
	    k = j - i;
	}

	i = 12;
	while( i > 0 ) {
        i--;
	}

/* ********************************* */


}
