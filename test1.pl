function putint(var in : int) : int {
    var out : int := in;

    if out < 10 {
        putchar(48 + in);
    }
    putint := in;
}

function f1(val in : float ): float {
    if in == 1.0 { f1 := 1; putchar(42); }
    else { f1 := in + f1 ( in - 1); putchar(43); }
}

function main (val argc: int, val argv : string):float {
    var a : float := 1.0;
    val s : string  ;
    var wh : float := 5.0;
    val bt : boolean := true;
    val bf : boolean := false;

    while wh > 0.0 {
        putchard(48.0 + wh);
        putchar(10);
        wh := wh - 1.0 ;
    }
    putchar(10);

    putchar(46);
    putchard(46.0);
    putchar(10);
    putint(4);
    putchar(10);
    if a != 1.0 {
         a := 2.0;
          } else { a := 0; }
    a := 1 + f1(a + 3);
    val b : float := a ;
    main := 5 * a - b;

    putchar(10); 
    if bt { putint(9); putchar(10);}
    if ! bf { putint(8); putchar(10);}
    if ! bt { putint(0);} else { putint(7);}
    putchar (10);

    puts("abc");
}
