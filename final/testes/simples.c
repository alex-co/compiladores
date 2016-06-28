
int    intv;
float  floatv;
char   chv;
string strv;
int    iglobal;
int d;

const float PI = 3.1415;
const int   UM = 1;

int functionc() {

    int    intv;
    float  f;
    float s;
    char   c;
    
    f = PI - 0.1415;
    s = 56.0 + '9';
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

    /* UM = 3; */
    /* y = 12; */
    /* m = n * o; */
    k = 3 * 12;
    k = 10 / j;
    /* i = j # k; */
    g = h # 3.14;
    /* g = h / 1.18; */
    i = j / k;
    /* g++; */
    /* m--; */
    
    if( g > h ) {
        i = j * k;
    }

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
