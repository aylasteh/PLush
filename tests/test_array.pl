
# function putint(var in : int) : int;

var global_i : int := 5;

function putint(var in : int) : int {
    var out : int := in;

    if out < 10 {
        putchar(48 + in);
    }
    putint := in;
}

function main (val argc: int, val argv : [string]):int {

    val array : [int] := {1, 2, 3, 6_01267, 11111_, 73567899};
    var array2D : [[int]] := {{1, 2}, {3, 4}, {5, 6}};
    var a1 : [int];
    val farray : [float] := {1.2, 2.2};
    var f1 : float;
    val sarray : [string] := { "abc", "def"};
    var a2 : [int] := {1,2,3};
    val i0 : int := 0;

    a2[i0] := 7;

    putchar(48 + a2[0]); putchar(10);

    f1 := farray[0];

    var i1 : int;

    a1 := array2D[1];

    puts(sarray[0]);
    puts(sarray[1]);

    putchar(48 + i1); putchar(10);

    i1 := array2D[2][0];
    putchar(48 + i1);  putchar(10);

    array2D[2][0] := 9;
    putchar(48 + array2D[2][0]);  putchar(10);

    putchar(48 + a1[0]); putchar(10);

    putchar(48 + global_i); putchar(10);

    print_int(10);
}
