from __future__ import print_function

from ctypes import CFUNCTYPE, c_double

import llvmlite.ir as ir
import llvmlite.binding as llvm

import ast_nodes

# get the semantic type
# in noe is set try the type
# otherwise None
def getsemtype(node):
    if hasattr(node, "sem_type"):
        if node.sem_type != None:
            return(node.sem_type)
    if hasattr(node, "type"):
        return(node.type)
    else:
        return None
class codeg(object):
    def __init__(self):
        self.module = ir.Module()
        self.builder = None
        self.func_symtab = {}

    def _create_entry_block_alloca(self, name, type):
        """Create an alloca in the entry BB of the current function."""
        builder = ir.IRBuilder()
        builder.position_at_start(self.builder.function.entry_basic_block)
        if type == "float":
            return builder.alloca(ir.DoubleType(), size=None, name=name)
        else:
            return builder.alloca(ir.IntType(32), size=None, name=name)

    def codegen(self, node):

        if isinstance(node, ast_nodes.IntExp):
            print(f"IntExp-semtype = {node.int} {node.sem_type}")
            if node.sem_type == "float":
                return ir.Constant(ir.DoubleType(), float(node.int))
            else:
                return ir.Constant(ir.IntType(32), node.int)
        
        elif isinstance(node, ast_nodes.FloatExp):
            return ir.Constant(ir.DoubleType(), float(node.value))

        elif isinstance(node, ast_nodes.IfExp):
                    # Emit comparison value
            cond_val = self.codegen(node.test)
            cmp = self.builder.fcmp_ordered(
                '!=', cond_val, ir.Constant(ir.DoubleType(), 0.0))

            # Create basic blocks to express the control flow, with a conditional
            # branch to either then_bb or else_bb depending on cmp. else_bb and
            # merge_bb are not yet attached to the function's list of BBs because
            # if a nested IfExpr is generated we want to have a reasonably nested
            # order of BBs generated into the function.
            then_bb = self.builder.function.append_basic_block('then')
            else_bb = ir.Block(self.builder.function, 'else')
            merge_bb = ir.Block(self.builder.function, 'ifcont')
            self.builder.cbranch(cmp, then_bb, else_bb)

            # Emit the 'then' part
            self.builder.position_at_start(then_bb)
            then_val = self.codegen(node.then_do)
            self.builder.branch(merge_bb)

            # Emission of then_val could have modified the current basic block. To
            # properly set up the PHI, remember which block the 'then' part ends in.
            then_bb = self.builder.block

            # Emit the 'else' part
            self.builder.function.basic_blocks.append(else_bb)
            self.builder.position_at_start(else_bb)
            if node.else_do != None:
                else_val = self.codegen(node.else_do)
            else:
                else_val = ir.Constant(ir.DoubleType(), float(1.0))

            # Emission of else_val could have modified the current basic block.
            else_bb = self.builder.block
            self.builder.branch(merge_bb)

            # Emit the merge ('ifcnt') block
            self.builder.function.basic_blocks.append(merge_bb)
            self.builder.position_at_start(merge_bb)
            phi = self.builder.phi(ir.DoubleType(), 'iftmp')
            phi.add_incoming(then_val, then_bb)
            phi.add_incoming(else_val, else_bb)
            return phi
    
        elif isinstance(node, ast_nodes.VarExp):
            var_addr = self.func_symtab[node.var]
            return self.builder.load(var_addr, node.var)
        elif isinstance(node, ast_nodes.AssignExp):
            if isinstance(node.var, ast_nodes.VarExp):
                var_addr = self.func_symtab[node.var.var]
            else:
                raise "Only simple variables are supportet"
            exp = self.codegen(node.exp)
            # print(node)
            self.builder.store(exp, var_addr)
            return exp
        elif isinstance(node, ast_nodes.ValVarDeclaration):
            old_bindings=[]
            
            if node.value != None:
                init_val = self.codegen(node.value)
            else:
                if node.type == "float":
                    init_val = ir.Constant(ir.DoubleType(), 0.0)
                else:
                    init_val = ir.Constant(ir.IntType(32), 0)
            
            saved_block = self.builder.block
            var_addr = self._create_entry_block_alloca(node.name, node.type)
            self.builder.position_at_end(saved_block)
            self.builder.store(init_val, var_addr)

            old_bindings.append(self.func_symtab.get(node.name))
            self.func_symtab[node.name] = var_addr
    
        elif isinstance(node, ast_nodes.FunctionCall):
            callee_func = self.module.get_global(node.name)
            if callee_func is None or not isinstance(callee_func, ir.Function):
                raise Exception('Call to unknown function', node.name)
            # if len(callee_func.args) != len(node.args):
            #    raise Exception('Call argument length mismatch', node.name)
            call_args = [self.codegen(arg) for arg in node.args.expr_list]
            #call_args = []
            print(f"callargs: {call_args}")
            return self.builder.call(callee_func, call_args, 'calltmp')
        elif isinstance(node, ast_nodes.ExpressionList):
            for n in node.expr_list:
                a = self.codegen(n)
                # print (a)
            return a
        elif isinstance(node, ast_nodes.FunctionDec):
            self.func_symtab = {}
            funcname = node.name
            # Create a function type
            arglist = []
            for iter in node.arg_types:
                if iter[1] == "float":
                    arglist = arglist + [ir.DoubleType()]
                else:
                    arglist = arglist + [ir.IntType(32)]
            print(f"ARGLIST: {arglist}")
            if node.return_type == "float":
                func_ty = ir.FunctionType(ir.DoubleType(),
                                    arglist)
            else:
                func_ty = ir.FunctionType(ir.IntType(32),
                                    arglist)
            func = ir.Function(self.module, func_ty, funcname)

            print(f"func: {func.args}")

            bb_entry = func.append_basic_block('entry')
            self.builder = ir.IRBuilder(bb_entry)

            print(f"func:arg_types {node.arg_types}")
            for i, iter in enumerate(func.args):
                if node.arg_types[i][1] == "float":
                    alloca = self.builder.alloca(ir.DoubleType(), name=node.arg_types[i][0])
                else:
                    alloca = self.builder.alloca(ir.IntType(32), name=node.arg_types[i][0])
                self.builder.store(iter, alloca)
                self.func_symtab[node.arg_types[i][0]] = alloca
                print(f"func args: {alloca}")

            if node.return_type == "float":            
                arg = ir.Constant(ir.DoubleType(), 0.0)
                alloca = self.builder.alloca(ir.DoubleType(), name=node.name)
            else:
                arg = ir.Constant(ir.IntType(32), 0)
                alloca = self.builder.alloca(ir.IntType(32), name=node.name)
            
            self.builder.store(arg, alloca)
            self.func_symtab[node.name] = alloca

            body = self.codegen(node.body)

            self.builder.ret(body)
            return func
        elif isinstance(node, ast_nodes.OpExp):
            print(f"opnode.semtype {node.sem_type}")
            left = self.codegen(node.left)
            leftsemtype = getsemtype(node.left)
            print(f"left semtype: {leftsemtype}")
            rightsemtype = getsemtype(node.left)
            print(f"right semtype: {rightsemtype}")
            right = self.codegen(node.right)
            if node.sem_type == "float":
                if node.oper == ast_nodes.Oper.plus:
                    return self.builder.fadd(left, right, 'addtmp')
                elif node.oper == ast_nodes.Oper.minus:
                    return self.builder.fsub(left, right, 'subtmp')
                elif node.oper == ast_nodes.Oper.times:
                    return self.builder.fmul(left, right, 'multmp')
            if node.sem_type == "boolean":
                if node.oper == ast_nodes.Oper.lt:
                    cmp = self.builder.fcmp_unordered('<', left, right, 'cmptmp')
                    return self.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')
                elif node.oper == ast_nodes.Oper.gt:
                    cmp = self.builder.fcmp_unordered('>', left, right, 'cmptmp')
                    return self.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')
                elif node.oper == ast_nodes.Oper.eq:
                    cmp = self.builder.fcmp_unordered('==', left, right, 'cmptmp')
                    return self.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')
                elif node.oper == ast_nodes.Oper.neq:
                    cmp = self.builder.fcmp_unordered('!=', left, right, 'cmptmp')
                    return self.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')
                elif node.oper == ast_nodes.Oper.ge:
                    cmp = self.builder.fcmp_unordered('>=', left, right, 'cmptmp')
                    return self.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')
                elif node.oper == ast_nodes.Oper.le:
                    cmp = self.builder.fcmp_unordered('<=', left, right, 'cmptmp')
                    return self.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')
                
            else:
                if node.oper == ast_nodes.Oper.plus:
                    return self.builder.add(left, right, 'addtmp')
                if node.oper == ast_nodes.Oper.minus:
                    return self.builder.sub(left, right, 'subtmp')
                if node.oper == ast_nodes.Oper.times:
                    return self.builder.mul(left, right, 'multmp')
            return(left)
        else:
            print("codegen not found: %s" % (type(node)))


