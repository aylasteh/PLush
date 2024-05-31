
from __future__ import print_function
from ctypes import CFUNCTYPE, c_int32, c_char_p

import llvmlite.ir as ir
import llvmlite.binding as llvm

from pathlib import Path
import argparse

import ast_nodes as Node
import plush_parser
import semantic
import codegen
import json

# ERROR
class SyntacticError(Exception):
    def __init__(self, value: str, position: int):
        self.value = value
        self.position = position

    def __str__(self):
        return f"Syntax error in input! Unexpected value {self.value} in line {self.position}"

def p_error(p):
    raise SyntacticError(p.value, p.lexer.lineno)

# Parsing the input string

#plush_program["minAndMax.pl"]
#plush_program["maxRangesquared.pl"]
plush_program="manipulateArrays.pl"
#plush_program["quicksort.pl"]
plush_program="test1.pl"
plush_program="test_str.pl"
plush_program="test_array.pl"

parsed_output = None

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="PLush file to parse")
arg_parser.add_argument("--tree", action="store_true", help="print syntax tree")
arg_parser.add_argument("--optimize", action="store_true", help="optimization")
arg_parser.add_argument("--showllvm", action="store_true", help="print generated llvm code")
arg_parser.add_argument("--showassembly", action="store_true", help="print generated llvm code after assembly stage")
arg_parser.add_argument("--execllvm", action="store_true", help="execute the generated object code in memory")

args = arg_parser.parse_args()

with open(args.file, 'r') as infile:
    input_string = infile.read()
try:
    parsed_output = plush_parser.plush_parse(input_string)

    if args.optimize:
        semantic.optimize = 1
    semantic.check(parsed_output)

    if args.tree:
        po = "{" + parsed_output.pp() + "}"
        jf = json.loads(po)
        print(json.dumps(jf, indent=2))

except SyntacticError as e:
    print(f"Syntax error: {e}")
    parsed_output = None
except Exception as e:
    print(f"Exception: {e}")
    parsed_output = None
        
if parsed_output == None:
    exit ()

# For now disable the llvm example

# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one
target = llvm.Target.from_default_triple()


cg = codegen.codeg()

llvm_ir = cg.codegen(parsed_output)

if args.showllvm:
    print(str(cg.module))

target_machine = target.create_target_machine(codemodel='small')

# Convert LLVM IR into in-memory representation
llvmmod = llvm.parse_assembly(str(cg.module))

plush_file_name=Path(args.file).stem
# Create object file
plush_object_file_name=plush_file_name + ".o"
with open(plush_object_file_name, 'wb') as obj_file:
    objdata = target_machine.emit_object(llvmmod)
    obj_file.write(objdata)
    # print('Wrote ' + plush_object_file_name)

if args.showassembly:
    print(llvmmod)

if args.execllvm:
    target_machine = target.create_target_machine()
    with llvm.create_mcjit_compiler(llvmmod, target_machine) as ee:
        ee.finalize_object()

        # print('======== Machine code')
        # print(target_machine.emit_assembly(llvmmod))

        fptr = CFUNCTYPE(c_int32)(ee.get_function_address("main"))
        args = (c_char_p * 2) (plush_file_name.encode(), b'arg1')
        result = fptr(len(args),  args )
        print(f"Result is: {result}")

exit()
