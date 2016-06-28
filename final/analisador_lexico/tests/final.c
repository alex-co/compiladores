int intv;
float floatv;
char chv;
string stringv;

const constc;

int do_int_stuff() {
   return 5 * intv + 3;
}

float do_float_stuff() {
   return 5.0 * floatv + 0;
}

char do_char_stuff() {
   return chv;
}

string do_string_stuff() {
   return stringv;
}

main {
   int intlocal       = do_int_stuff();
   float floatlocal   = do_float_stuff();
   char charlocal     = do_char_stuff();
   string stringlocal = do_string_stuff();

   char problematico;


   if (intlocal >= floatlocal)
      intlocal = intv;

   while (floatlocal <= intlocal && floatlocal )
      intlocal++;

   if (intlocal == floatlocal || intlocal <= floatlocal) {
      charlocal = 'i'
   }

   for (intlocal = 0; intlocal < floatlocal; inlocal++)
      floatlocal++;
}
