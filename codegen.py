from __future__ import print_function

from ctypes import CFUNCTYPE, c_double

import llvmlite.ir as ir
import llvmlite.binding as llvm

import ast_nodes

class codeg(object):
    def __init__(self):
        self.module = ir.Module()
        self.builder = None
        self.func_symtab = {}


    def codegen(self, node):

        if isinstance(node, ast_nodes.IntExp):
            return ir.Constant(ir.DoubleType(), float(node.int))

        elif isinstance(node, ast_nodes.VarExp):
            return
        elif isinstance(node, ast_nodes.AssignExp):
            v = self.codegen(node.var)
            exp = self.codegen(node.exp)
            return exp
        elif isinstance(node, ast_nodes.ExpressionList):
            return self.codegen(node.expr_list[0])
        elif isinstance(node, ast_nodes.FunctionDec):
            funcname = node.name
            # Create a function type
            func_ty = ir.FunctionType(ir.DoubleType(),
                                    [ir.DoubleType()] * 0)
            func = ir.Function(self.module, func_ty, funcname)
            bb_entry = func.append_basic_block('entry')
            self.builder = ir.IRBuilder(bb_entry)
            print("Builder assigned")
            body = self.codegen(node.body)
            self.builder.ret(body)
            return func
        elif isinstance(node, ast_nodes.OpExp):
            left = self.codegen(node.left)
            right = self.codegen(node.right)
            print(left)
            print(right)
            if node.oper == ast_nodes.Oper.times:
                return self.builder.fmul(left, right, 'multmp')
            return(left)
        else:
            print("codegen: " % (type(node)))


