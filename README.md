author: Ayla Stehling (fc63327)

## structure:
ast_nodes.py -> nodes of ast of language <br/>
codegen.py -> ir code generation using llvmlite <br/>
lex.py -> tokens of language <br/>
plush_parser.py -> parser of language <br/>
plush.py -> compile llvm <br/>
semantic.py -> semantics of language <br/>
folder src/ply -> contains tools yacc.py and lex.py <br/>
folder tests -> contains all tests <br/>
setup.sh -> install all dependencies on the latest Ubuntu LTS <br/>
splush -> script to run code

tests/examples are in the tests folder, see README.md in folder for more information

## how to run:
run setup.sh on the latest Ubuntu LTS release to install all dependencies <br/>
tested with ubuntu:20.04 image started using docker run -it --name ubuntu20 ubuntu:20.04 bash <br/>

./splush "filename".pl  -> create .o and executable  <br/>
./splush --tree "filename".pl -> prints abstract syntax tree <br/>
    (When trying out this function I would recommend not using it on the longest programm as the AST can get quite long. A recommended test programm is example1.pl) <br/>
./splush --optimize "filename".pl -> wenn used to execute file, the tree optimizers will be applied <br/>

./"filename" -> run file

note:  <br/>
if llvm missing, check the path to python (line 10 in splush)

# PLush
PLush compiler

Language Description:

- Comments in PLush start with # and end at the end of the line.
- PLush is whitespace insensitive.
- A program is made of several declarations or definitions that precede the main body.
- A declaration includes the name of the function, its arguments and types and refinements, as well as the return type.

<p align="center">
val x : int := 1;
</p>

- Top-level declarations can be definitions of constants (val), definitions of mutable variables (var) or definition of functions.
- Types are either boolean, char, float, int, string, void, or parametric arrays: [double], [int], [[int]]
- Functions can be defined, or declared, depending on whether there is a body of code, or a semi-colon.
- A definition is similar, but includes a block of code that defines the function, or a definition of the value.

<p align="center">
var a : int := 1; <br />
val b : int := 2; <br />
function f(val x : int) : int { f := x ^ 2; } <br />
function g(val x : int) : float; # declaration of function for FFI.
</p>

- Statements, declarations and definitions (except functions) with values end with semicolon. Definitions of functions do not need semicolon, as the curly braces delimit the function.
- Blocks are enclosed with { and } and are comprised of 0 or more statements.
- If statements have a condition, a then block and optionally an else block, separated by the else keyword.
- While statements are similar to if statements, without the else block.
- Local variables statements are defined similarly to global ones (with a mandatory starting value)
- Variable assignments can be statements (a := 2);
- Expressions represent values. They can be:
 
    - Binary operators, with a C-like precedence and parenthesis to force other precedences: `&&`, `||`, `=`, `!=`, `>=`, `>`, `<=`, `<`, `+`, `-`, `*`, `/`, `%` em que a divisão tem sempre a semântica da divisão de floats.
    - The not unary operator (!true)
    - Boolean literals (`true`, `false`)
    - Integer literals (`1`, `01`, `12312341341`, `1_000_000`) where underscores can be present in any position.
    - Float literals (`1.1`, `.5`, `1233123131231321`)
    - String literals (`""`, `"a"`, `"aa"`, `"qwertyuiop"`, `"qwerty\tuiop"`)
    - Variables, which start with a letter or understore and are followed by any number of letters, underscores or numbers.
    - index access, (`a[0]` or `get_array()[i+1]`)