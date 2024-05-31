
# Global variable 
var global_i : int := 5;

# Function prototpe
function putint(var in : int) : int;

# Another global variable
var global_3 : int := 3;

function main (val argc: int, val argv : [string]):int {
    var str : string;

    putchar(48 + global_i); putchar(10);

    putchar(48 + argc); putchar(10);

    var i : int := 0;

    puts(argv[0]);

    while i < argc {
        puts(argv[i]);
        i := i + 1;
    }

    putint(global_3); 
    putchar(10);

    main := 0;
}

# function definition (from prototype)
function putint(var in : int) : int {
    var out : int := in;

    if out < 10 {
        putchar(48 + in);
    }
    putint := in;
}