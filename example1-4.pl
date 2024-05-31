val num : int := 100.3; # declared int, but is a float 
val modu : int := 8;

function modulo(var numb:int, val mod:int) : int{
    while numb > mod {
        var temp : int := numb;
        numb := temp - mod;
    }
    modulo := numb;
}

function main(val args: string):int{
    val result : int := modulo(num,modu);
    main := result;
}