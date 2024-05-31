val num : int := 100;
val modu : int := 8;

function modulo(var numb:int, val mod:int) : int{
    while numb > mod {
        var temp : int := numb;
        numb := temp -- mod; # minus too much
    }
    modulo := numb;
}

function main(val args: string):int{
    val result : int := modulo(num,modu);
    print_int(result);
}