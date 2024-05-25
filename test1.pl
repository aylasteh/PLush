
function f1(val in : float ): float {
    if in == 1.0 { f1 := 1; }
    else { f1 := in + f1 ( in - 1);}
    f1 := f1;
}

function main ():float {
    var a : float := 1.0;

    if a != 1.0 {
         a := 2.0;
          } else { a := 0; }
    a := 1 + f1(a + 3);
    val b : float := a ;
    main := 5 * a - b;
}
