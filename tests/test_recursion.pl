# Test recursion

function fibonacci(val in : int ): int {
    if in == 0 { 
        fibonacci :=0; }
    else { 
        if in == 1 {
            fibonacci := 1;
        }
        else {
            var l: int := fibonacci(in - 1);
            var r: int := fibonacci(in - 2);

            fibonacci := l + r;
        }
    }
}

function main (val argc: int, val argv : [string]):int {
    var i : int := 0;

    while i < 10 {
        print_int(fibonacci(i));
        i := i + 1;
    }
    main :=  0;
}