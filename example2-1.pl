val a : int := 55;
val b : int := 967;

function gct(var a1:int, var b1:int) : string {
    if a1 == 0 {
        gct := b1;
    } else {
        while b1 > 0 {
            if a1 > b1 {
                a1 := a1 - b1;
            } else {
                b1 := b1 - a1;
            }
        }
    }
    gct := a1;
}

function main(val args: string) :int {
    val result : int := gct(a,b); # gct returns a string, but is saved here as an int
    main := result;
}

