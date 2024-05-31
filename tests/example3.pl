val fib : int := 7;

function getNthFib(var n:int) : int {
    var res: int := 0;
    if n == 1 {
        res := 0;
    } else {
        if n == 2 {
        res := 1;
        } else {
            var presPrev: int := 0;
            var prev: int := 1;
            var currentNumber: int := 0;
            var counter: int := 2;
            while counter < n {
                currentNumber := presPrev + prev;
                presPrev := prev;
                prev := currentNumber;
                counter := counter + 1;
            }
            res := currentNumber;
        }
    }
    
    getNthFib := res;

}

function main(val args: string):int{
    val result : int := getNthFib(fib);
    print_int(result);
}