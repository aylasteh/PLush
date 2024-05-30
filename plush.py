
from __future__ import print_function
from ctypes import CFUNCTYPE, c_double

import llvmlite.ir as ir
import llvmlite.binding as llvm

from pathlib import Path
import argparse

import ast_nodes as Node
import plush_parser
import semantic
import codegen

import jsonpickle


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

args = arg_parser.parse_args()

with open(args.file, 'r') as infile:
    input_string = infile.read()
try:
    parsed_output = plush_parser.plush_parse(input_string)
    if args.tree:
        print("Parsed output:")


    if args.optimize:
        semantic.optimize = 1
    semantic.check(parsed_output)
    if args.tree:
        print(jsonpickle.encode(parsed_output))

except SyntacticError as e:
    print(f"Syntax error: {e}")
    parsed_output = None
except Exception as e:
    print("Exception:")
    print(e)
    print(type(e))
    parsed_output = None
    print("Continuing with next file")
        
if parsed_output == None:
    print("error parsing")
    exit ()



# For now disable the llvm example

# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one
target = llvm.Target.from_default_triple()


cg = codegen.codeg()

llvm_ir = cg.codegen(parsed_output)

print(str(cg.module))

target_machine = target.create_target_machine(codemodel='small')

# Convert LLVM IR into in-memory representation
llvmmod = llvm.parse_assembly(str(cg.module))

# Create object file
plush_object_file_name=Path(args.file).stem + ".o"
with open(plush_object_file_name, 'wb') as obj_file:
    #llvmassembly = target_machine._assembly(llvmmod)
    objdata = target_machine.emit_object(llvmmod)
    obj_file.write(objdata)
    # print('Wrote ' + plush_object_file_name)

#print(llvmmod)

target_machine = target.create_target_machine()
with llvm.create_mcjit_compiler(llvmmod, target_machine) as ee:
    ee.finalize_object()

    # print('======== Machine code')
    # print(target_machine.emit_assembly(llvmmod))

    fptr = CFUNCTYPE(c_double)(ee.get_function_address("main"))
    result = fptr()
    print(f"Result is: {result}")



exit()

llvm_ir = """
   ; ModuleID = "examples/ir_fpadd.py"
   target triple = "unknown-unknown-unknown"
   target datalayout = ""

   define double @"fpadd"(double %".1", double %".2")
   {
   entry:
     %"res" = fadd double %".1", %".2"
     ret double %"res"
   }
   """

def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod


engine = create_execution_engine()
mod = compile_ir(engine, llvm_ir)

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("fpadd")

# Run the function via ctypes
cfunc = CFUNCTYPE(c_double, c_double, c_double)(func_ptr)
res = cfunc(1.0, 3.5)
print("fpadd(...) =", res)
