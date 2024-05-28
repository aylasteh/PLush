
function main (val argc: int, val argv : string):float {

    val s : string := "abc";
    val s1 : string := "efghi";
    var s2 : string := s;

    s2 := s1;

    puts(s);
    puts(s2);
    puts("hello");
    putchar(48);
    putchar(10);

    main := 9;

}