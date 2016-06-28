
int    intv;
float  floatv;
char   chv;
string strv;
int    iglobal;

const float PI = 3.1415;
const int   UM = 1;

int functionc() {

    int    d;
    float  f;
    string s;
    char   c;

	f = PI - 0.1415;
	s = "abc";
    c = 'a';
    d = 2;
    d = d + 3;

    return UM;
}

main {
    int    i;
    int    j;
    int    k;
    char   c;
    char   d;
    float  g;
    float  h;
    string m;
    string n;
    string o;

	j = 2;
	k = 22;
	i = k - j;
	i = i - 10;
	i = k / 2;

    /* Atribuição para constante */
    /* UM = 3; */

    /* 'y' não foi declarado */
    /* y = 12; */

    /* Atribuição de tipos diferentes */
    /* int   e;
    char  c;
    float f;
    c = 'a';
    e = c;
    i = 22; */

    /* *** Operador aritmético em um tipo não numérico *** */
    /* m = n * o; */
    k = 3 * 12;
    k = 10 / j;

    /* k = 9 % 3; => ERRO no analisador sintático <= */

    /* *** Operador de ponto flutuante aplicado a inteiro *** */
    /* i = j # k; */
    g = h # 3.14;

    /* *** Operador de inteiro aplicado a ponto flutuante *** */
    /* g = h / 1.18; */
    i = j / k;

    /* *** Incremento aplicado a ponto flutuante *** */
    /* g++; */

    /* *** Decremento aplicado a string *** */
    /* m--; */

    j = 2; j--;
    k = i + j;
    if( i >= 1 && j < 10 ) {
        k = j + 1;
    }
    for( i = 0; i <= j; i++ ) {
	    k = j - i;
	}
	i = 12;
	while( i > 0 ) {
        i--;
	}
}
