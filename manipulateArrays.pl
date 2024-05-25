val constant__123_ : int := 1_000;

function create_array(val N:int) : [int];

# Pre condition: forall x in array ==> array[x] >= 1_000
function subtractUntilNegative(var array:[int], val length:int) : int {
    val initialArray : [int] := array;
    var index : int := -1;
    var _isNegative__ : boolean := false;
    while !_isNegative__ {
        var i : int := 1;
        while i <= length {
            if array[i - 1] % 2 == 0 || array[i - 1] % 3 == 0 {
                array[i - 1] := array[i - 1] - constant__123_;
            } else {
                array[i - 1] := array[i - 1] - (constant__123_ * .5);
            }
            if array[i - 1] < 0 {
                _isNegative__ := true;
                index := i - 1;
            }
            i := i + 1;
        }
    }
    
    
    subtractUntilNegative := initialArray[index];
}

function turn2Dinto1D(var array2D: [[int]], val row: int, val length0:int) : [int] {
    var array1D : [int] := create_array(length0);
    var col : int := 0;
    while col < length0 {
        array1D[col] := array2D[row][col];
        col := col + 1;
    }
    turn2Dinto1D := array1D;
}

function subtractUntilNegative2D(var array2D:[[int]], val numRows:int, val numCols:int) : [int] {
    var row : int := 0;
    var array1D : [int] := create_array(numRows);
    var index : int := 0;
    while row < numRows {
        val _2Dinto1D : [int] := turn2Dinto1D(array2D, row, numCols);
        array1D[index] := subtractUntilNegative(_2Dinto1D, numCols);
        index := index + 1;
    }
    subtractUntilNegative2D := array1D;
}


function invertOne(var array: [int], val length:int) : [int]{
    var firstValue : int := array[0];
    array[0] := array[length - 1];
	array[length - 1] := firstValue;
	invertOne := array;
}

function main(val args:[string]) {
    
    #Test array 1D
    val array : [int] := {1_0000_0, 5000_0631, 12312341341, 6_01267, 11111_, 73567899};
	val N : int := 6;
	val result : int := subtractUntilNegative(invertOne(array, N), N);
	print_int(result);
    
    #Test array 2D
    val array2D : [[int]] := {{1_0000_0, 5000_0631}, {12312341341, 6_01267}, {11111_, 73567899}};
    var result_array : [int] := subtractUntilNegative2D(array2D, 3, 2);
	val result_2D : int := subtractUntilNegative(result_array, 6);
	print_int(result_2D);
}

function main1(val args:[string]) ;