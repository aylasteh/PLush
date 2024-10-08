from __future__ import print_function

from ctypes import CFUNCTYPE, c_double

import llvmlite.ir as ir
import llvmlite.binding as llvm

import ast_nodes

type_bool  = ir.IntType(1)
type_i8  = ir.IntType(8)
type_i32 =  ir.IntType(32)
type_dbl = ir.DoubleType()
type_pi8 = type_i8.as_pointer()
type_char = type_i8
type_str = type_char.as_pointer()
type_pi32 = type_i32.as_pointer()


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

def get_pointertype_fromArrayExp(node):
    if isinstance(node.type, ast_nodes.ArrayExp):
        return ir.ArrayType(get_pointertype_fromArrayExp(node.type).as_pointer(), 1)
    else:
        if node.type == "float":
            return ir.ArrayType(type_dbl, 1)
        elif node.type == "string":
            return ir.ArrayType(type_str, 1)
        elif node.type == "boolean":
            return ir.ArrayType(type_bool, 1)
        else:
            return ir.ArrayType(type_i32, 1)

def get_llvmtype_fromArglist(intype):
    if isinstance(intype, list):
        if isinstance(intype[0], list):
            return ir.ArrayType(get_llvmtype_fromArglist(intype[0]).as_pointer(), 1)
        else:
            return ir.ArrayType(get_llvmtype_fromArglist(intype[0]), 1).as_pointer()
    else:
        if intype == "float":
           return (type_dbl)
        elif intype == "string":
            return (type_str)
        elif intype == "boolean":
            return (type_bool)
        else:
            return (type_i32)
                                  
class codeg(object):
    def __init__(self):
        self.module = ir.Module()
        self.builder = None
        self.func_symtab = None
        self.count = 0
        self.add_builtins(self.module)

    def add_builtins(self, module):
        # The C++ tutorial adds putchard() simply by defining it in the host C++
        # code, which is then accessible to the JIT. It doesn't work as simply
        # for us; but luckily it's very easy to define new "C level" functions
        # for our JITed code to use - just emit them as LLVM IR. This is what
        # this method does.

        # Add the declaration of puts
        puts_ty = ir.FunctionType(type_i32, [type_str])
        puts = ir.Function(module, puts_ty, 'puts')

        # Add the declaration of putchar
        putchar_ty = ir.FunctionType(type_i32, [type_i32])
        putchar = ir.Function(module, putchar_ty, 'putchar')

        # Add the print_int

        intfmt = "%d\n"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(intfmt) +1),
                        bytearray(intfmt.encode("utf8")) + b'\x00')
        global_fmt = ir.GlobalVariable(module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        printf_ty = ir.FunctionType(ir.IntType(32), [type_pi8], var_arg=True)
        printf = ir.Function(module, printf_ty, name="printf")
        print_int_ty = ir.FunctionType(type_dbl, [type_i32])
        print_int = ir.Function(module, print_int_ty, 'print_int')
        irbuilder = ir.IRBuilder(print_int.append_basic_block('entry'))
        fmt_arg = irbuilder.bitcast(global_fmt, type_pi8)
        irbuilder.call(printf, [fmt_arg,print_int.args[0]] )
        irbuilder.ret(ir.Constant(type_dbl, 0))

        # Add putchard
        putchard_ty = ir.FunctionType(type_dbl, [type_dbl])
        putchard = ir.Function(module, putchard_ty, 'putchard')
        irbuilder = ir.IRBuilder(putchard.append_basic_block('entry'))
        ival = irbuilder.fptoui(putchard.args[0], type_i32, 'intcast')
        irbuilder.call(putchar, [ival])
        irbuilder.ret(ir.Constant(type_dbl, 0))

    def _create_global(self, name, type):
        """Create global variable."""
        #print(f"alloca {type}")
        if type == "float":
            return ir.GlobalVariable(self.module, type_dbl, name=name)
        elif type == "string":
            return ir.GlobalVariable(self.module, type_str, name=name)
        elif type == "boolean":
            return ir.GlobalVariable(self.module, type_bool, name=name)
        elif isinstance(type, ast_nodes.ArrayExp):
            return ir.GlobalVariable(self.module, get_pointertype_fromArrayExp(type).as_pointer(), size=None, name=name)
        else:  # boolean and int
            return ir.GlobalVariable(self.module, type_i32, name=name)
                                           
    def _create_entry_block_alloca(self, name, type):
        """Create an alloca in the entry BB of the current function."""
        builder = ir.IRBuilder()
        builder.position_at_start(self.builder.function.entry_basic_block)
        #print(f"alloca {type}")
        if type == "float":
            return builder.alloca(type_dbl, size=None, name=name)
        elif type == "string":
            return builder.alloca(type_str, size=None, name=name)
        elif type == "boolean":
            return builder.alloca(type_bool, size=None, name=name)
        elif isinstance(type, ast_nodes.ArrayExp):
            return builder.alloca(get_pointertype_fromArrayExp(type).as_pointer(), size=None, name=name)
        else:  # boolean and int
            return builder.alloca(type_i32, size=None, name=name)

    def get_var_addr(self, var_name):
        # get address of variable from local or global
        # first check local
        if var_name in self.func_symtab:
            return self.func_symtab[var_name]
        return self.module.get_global(var_name)

    def codegen(self, node):

        if isinstance(node, ast_nodes.IntExp):
            # print(f"IntExp-semtype = {node.int} {node.sem_type}")
            if node.sem_type == "float":
                return ir.Constant(type_dbl, float(node.int))
            else:
                return ir.Constant(type_i32, node.int)
        
        elif isinstance(node, ast_nodes.FloatExp):
            return ir.Constant(type_dbl, float(node.value))
        
        elif isinstance(node, ast_nodes.BoolExp):
            return ir.Constant(type_bool, 1 if node.value == True else 0)
        
        elif isinstance(node, ast_nodes.StringExp):
            # strings are a pointer to int(8)
            # allocate the space Global
            # then gep will work. gep returns the pointer to an index
            loc_type = ir.ArrayType(type_char, len(node.string) + 1)                            
            location= ir.Constant(loc_type, bytearray(node.string.encode()) + b'\x00')
            nl = ir.GlobalVariable(self.module, loc_type, name="string."+str(self.count))
            self.count = self.count + 1
            nl.initializer=location
            nl.global_constant=True
            d = nl.gep([ir.Constant(type_char, 0)]).bitcast(type_str)
            return d


        elif isinstance(node, ast_nodes.WhileExp):
        
            saved_block = self.builder.block

            loop_bb = self.builder.function.append_basic_block('loop')

            # Insert an explicit fall through from the current block to loop_bb
            self.builder.branch(loop_bb)
            self.builder.position_at_start(loop_bb)

            # Emit the body of the loop. This, like any other expr, can change the
            # current BB. Note that we ignore the value computed by the body.
            body_val = self.codegen(node.body)

            # Compute the end condition
            endcond = self.codegen(node.test)
            cmp = self.builder.icmp_signed(
                '!=', endcond, ir.Constant(type_bool, 0),
                'loopcond')

            # Create the 'after loop' block and insert it
            after_bb = self.builder.function.append_basic_block('afterloop')

            # Insert the conditional branch into the end of loop_end_bb
            self.builder.cbranch(cmp, loop_bb, after_bb)

            # New code will be inserted into after_bb
            self.builder.position_at_start(after_bb)

            # The 'while' expression always returns 0
            return ir.Constant(type_i32, 0)
    
        elif isinstance(node, ast_nodes.IfExp):
                    # Emit comparison value
            cond_val = self.codegen(node.test)
            cmp = self.builder.icmp_signed(
                '!=', cond_val, ir.Constant(type_bool, 0))

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
            then_val = ir.Constant(type_i32, 0)
            self.builder.branch(merge_bb)

            # Emission of then_val could have modified the current basic block. To
            # properly set up the PHI, remember which block the 'then' part ends in.
            then_bb = self.builder.block

            # Emit the 'else' part
            self.builder.function.basic_blocks.append(else_bb)
            self.builder.position_at_start(else_bb)
            if node.else_do != None:
                else_val = self.codegen(node.else_do)
                else_val = ir.Constant(type_i32, 0)
            else:
                else_val = ir.Constant(type_i32, 0)

            # Emission of else_val could have modified the current basic block.
            else_bb = self.builder.block
            self.builder.branch(merge_bb)

            # Emit the merge ('ifcnt') block
            self.builder.function.basic_blocks.append(merge_bb)
            self.builder.position_at_start(merge_bb)
            phi = self.builder.phi(type_i32, 'iftmp')
            phi.add_incoming(then_val, then_bb)
            phi.add_incoming(else_val, else_bb)
            return phi
    
        elif isinstance(node, ast_nodes.VarExp):
            var_addr = self.get_var_addr(node.var)
            return self.builder.load(var_addr, node.var)
        elif isinstance(node, ast_nodes.ArrayExp):
            obj_reference = self.get_var_addr(node.type)
            for i in node.size.expr_list:
                pos = self.codegen(node.size.expr_list[0])
                xx=self.builder.load(obj_reference)
                obj_reference =self.builder.gep(xx, [ir.Constant(type_i32, 0), pos])     
            obj_reference = self.builder.load(obj_reference)
            return obj_reference
        elif isinstance(node, ast_nodes.AssignExp):
            if isinstance(node.var, ast_nodes.VarExp):
                # left side is simple variable
                var_addr = self.get_var_addr(node.var.var)
            elif isinstance(node.var, ast_nodes.ArrayExp):
                # left side is array with index a[]
                # this code is sort of duplicated from above difference is the missing load()
                ae = node.var
                obj_reference = self.get_var_addr(ae.type)
                for i in ae.size.expr_list:
                    pos = self.codegen(i)
                    xx=self.builder.load(obj_reference)
                    obj_reference =self.builder.gep(xx, [ir.Constant(type_i32, 0), pos])     
                var_addr = obj_reference
            else:
                raise f"Only variables on left side of expression are supported got {node.var}"
            exp = self.codegen(node.exp)
            self.builder.store(exp, var_addr)
            return exp
        elif isinstance(node, ast_nodes.ValVarDeclaration):
            old_bindings=[]

            # allocate space for the variables.
            if node.value != None:
                # initializer 
                init_val = self.codegen(node.value)
            else:
                # default space
                if node.type == "float":
                    init_val = ir.Constant(type_dbl, None)
                elif node.type == "string":
                    init_val = ir.Constant(type_str, None)  
                elif node.type == "boolean":
                    init_val = ir.Constant(type_bool, None) 
                elif isinstance(node.type, ast_nodes.ArrayExp):
                    init_val= ir.Constant(get_pointertype_fromArrayExp(node.type).as_pointer(), None)
                else:
                    # integer of boolean
                    init_val = ir.Constant(type_i32, None)
            
            
            if self.func_symtab == None:
                # in global context
                var_addr = self._create_global(node.name, node.type)
                var_addr.initializer = init_val
            else:
                # local vars
                # create and store reference in symbol table
                saved_block = self.builder.block
                var_addr = self._create_entry_block_alloca(node.name, node.type)
                self.builder.position_at_end(saved_block)
                # print(self.module)
                # print(f"store: {init_val} -> {var_addr}")
                self.builder.store(init_val, var_addr)
                old_bindings.append(self.func_symtab.get(node.name))
                self.func_symtab[node.name] = var_addr
    
        elif isinstance(node, ast_nodes.FunctionCall):
            callee_func = self.module.get_global(node.name)
            if callee_func is None or not isinstance(callee_func, ir.Function):
                raise Exception('Call to unknown function', node.name)
            if not isinstance(node.args, ast_nodes.EmptyExp):
                if len(callee_func.args) != len(node.args.declaration_list):
                    raise Exception('Call argument length mismatch', node.name)
            else:
                if len(callee_func.args) != 0:
                    raise Exception('Call argument length mismatch', node.name)
            
            if not isinstance(node.args, ast_nodes.EmptyExp):
                call_args = [self.codegen(arg) for arg in node.args.declaration_list]
            else:
                call_args = []
            # print(f"callargs: {call_args}")
            return self.builder.call(callee_func, call_args, 'calltmp')
        
        elif isinstance(node, ast_nodes.ExpressionList):
            for n in node.expr_list:
                a = self.codegen(n)
            return a
        
        elif isinstance(node, ast_nodes.DeclarationBlock):
            # Here we have to initialize the array....
            dim = node.dimension[0]
            for i, n in enumerate(node.declaration_list):    
                a = self.codegen(n)
                if i == 0:
                    arr_type = ir.ArrayType(a.type, 1)
                    p = self.builder.alloca(arr_type, dim )
                    # print(p)
                pp = self.builder.gep(p, [ir.Constant(type_i32,0), ir.Constant(type_i32,i)])
                self.builder.store(a, pp)
                #print(pp)
            return p
        
        elif isinstance(node, ast_nodes.FunctionDec):  
            old_symtab = self.func_symtab  
            self.func_symtab = {}

            funcname = node.name
            # Create a function type
            arglist = []
            for iter in node.arg_types:
                ltype = get_llvmtype_fromArglist(iter[1])
                arglist = arglist + [ltype]
            # print(f"ARGLIST: {arglist}")
            if node.return_type == "float":
                func_ty = ir.FunctionType(type_dbl,
                                    arglist)
            elif node.return_type == "string":
                # func_ty = ir.FunctionType(ir.ArrayType(ir.IntType(8),8), arglist)
                func_ty = ir.FunctionType(type_str, arglist)
            elif node.return_type == "boolean":
                func_ty = ir.FunctionType(type_bool, arglist)
            else:
                func_ty = ir.FunctionType(type_i32,
                                    arglist)
            
            if funcname in self.module.globals:
                # there was already a declaration
                func = self.module.globals[funcname]
            else:
                func = ir.Function(self.module, func_ty, funcname)

            # print(f"func: {func.args}")

            if node.body == None:
                # this is the declaration only.
                self.func_symtab = old_symtab
                return func

            bb_entry = func.append_basic_block('entry')
            self.builder = ir.IRBuilder(bb_entry)

            #print(f"func:arg_types {node.arg_types}")
            for i, iter in enumerate(func.args):
                # print(f"{arglist[i]}, {node.arg_types[i][0]}")
                alloca = self.builder.alloca(arglist[i],  name=node.arg_types[i][0])
                self.builder.store(iter, alloca)
                self.func_symtab[node.arg_types[i][0]] = alloca
                # print(f"func args: {alloca}")

            if node.return_type != None:
                # allocate space for the return type
                rt = get_llvmtype_fromArglist(node.return_type)
                arg = ir.Constant(rt, None)
                func_var = self.builder.alloca(rt, name=node.name)

                self.builder.store(arg, func_var)
                self.func_symtab[node.name] = func_var

            body = self.codegen(node.body)

            if node.return_type != None:
                self.builder.ret(self.builder.load(func_var, node.name))
            else:
                self.builder.ret_void()
            
            self.func_symtab = old_symtab
            return func
            
        elif isinstance(node, ast_nodes.OpExp):
            # print(f"opnode.semtype {node.sem_type}")

            if hasattr(node, "opt") and node.opt != None:
                # optimizer
                return(ir.Constant(type_i32, node.opt))

            # print(f"right semtype: {rightsemtype}")
            right = self.codegen(node.right)
            rightsemtype = getsemtype(node.left)
            if rightsemtype == None:
                if right.type == type_dbl:
                    rightsemtype = "float"
            
            if node.oper != ast_nodes.Oper.notop:
                left = self.codegen(node.left)
                leftsemtype = getsemtype(node.left)
                if leftsemtype == None:
                    if left.type == type_dbl:
                        leftsemtype = "float"
                # print(f"left semtype: {leftsemtype}")
            else:
                if right.type != type_bool:
                    return self.builder.icmp_unsigned('!=', ir.Constant(type_i32, 1), right, 'nottmp')
                else:
                    return self.builder.icmp_unsigned('!=', ir.Constant(type_bool, 1), right, 'nottmp')
            
            if node.oper == ast_nodes.Oper.andop:
                if leftsemtype == "float":
                    lr = self.builder.fcmp_unordered('!=', ir.Constant(type_dbl, 0.0), left, 'fandtmplr')
                    rr = self.builder.fcmp_unordered('!=', ir.Constant(type_dbl, 0.0), right, 'fandtmprr')
                else:
                    print(left.type)
                    if left.type != type_bool:
                        lr = self.builder.icmp_unsigned('!=', ir.Constant(type_i32, 0), left, 'andtmplr')
                    else:
                        lr = left
                    if right.type != type_bool:
                        rr = self.builder.icmp_unsigned('!=', ir.Constant(type_i32, 0), left, 'ortmplr')
                    else:
                        rr = right
                cmp = self.builder.and_(lr, rr, 'andaddtmp')
                #cmp = self.builder.icmp_unsigned('==', cmpr, ir.Constant(type_i32, 2), 'andcmptmp')
                return cmp
            if node.oper == ast_nodes.Oper.orop:
                if leftsemtype == "float":
                    lr = self.builder.fcmp_unordered('!=', ir.Constant(type_dbl, 0.0), left, 'andtmplr')
                    rr = self.builder.fcmp_unordered('!=', ir.Constant(type_dbl, 0.0), right, 'andtmprr')
                else:
                    if left.type != type_bool:
                        lr = self.builder.icmp_unsigned('!=', ir.Constant(type_i32, 0), left, 'ortmplr')
                    else:
                        lr = left
                    if right.type != type_bool:
                        rr = self.builder.icmp_unsigned('!=', ir.Constant(type_i32, 0), left, 'ortmplr')
                    else:
                        rr = right
                cmp = self.builder.or_(lr, rr, 'oraddtmp')
                # cmp = self.builder.icmp_unsigned('>', cmpr, ir.Constant(type_i32, 0), 'orcmptmp')
                return cmp
                
            
            if node.sem_type == "float":
                if node.oper == ast_nodes.Oper.plus:
                    return self.builder.fadd(left, right, 'addtmp')
                elif node.oper == ast_nodes.Oper.minus:
                    return self.builder.fsub(left, right, 'subtmp')
                elif node.oper == ast_nodes.Oper.times:
                    return self.builder.fmul(left, right, 'multmp')
                elif node.oper == ast_nodes.Oper.divide:
                    return self.builder.fdiv(left, right, 'divtmp')
                elif node.oper == ast_nodes.Oper.exponent:
                    powi = self.module.declare_intrinsic('llvm.pow', [type_dbl])
                    return self.builder.call(powi, [left, right], 'fcall')
                
            if node.sem_type == "boolean":
                if leftsemtype == "float":
                    if node.oper == ast_nodes.Oper.lt:
                        cmp = self.builder.fcmp_unordered('<', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.gt:
                        cmp = self.builder.fcmp_unordered('>', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.eq:
                        cmp = self.builder.fcmp_unordered('==', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.neq:
                        cmp = self.builder.fcmp_unordered('!=', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.ge:
                        cmp = self.builder.fcmp_unordered('>=', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.le:
                        cmp = self.builder.fcmp_unordered('<=', left, right, 'cmptmp')
                        return cmp


                else:
                    if node.oper == ast_nodes.Oper.lt:
                        cmp = self.builder.icmp_unsigned('<', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.gt:
                        cmp = self.builder.icmp_unsigned('>', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.eq:
                        cmp = self.builder.icmp_unsigned('==', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.neq:
                        cmp = self.builder.icmp_unsigned('!=', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.ge:
                        cmp = self.builder.icmp_unsigned('>=', left, right, 'cmptmp')
                        return cmp
                    elif node.oper == ast_nodes.Oper.le:
                        cmp = self.builder.icmp_unsigned('<=', left, right, 'cmptmp')
                        return cmp
                
            else:
                if node.oper == ast_nodes.Oper.plus:
                    return self.builder.add(left, right, 'addtmp')
                if node.oper == ast_nodes.Oper.minus:
                    return self.builder.sub(left, right, 'subtmp')
                if node.oper == ast_nodes.Oper.times:
                    return self.builder.mul(left, right, 'multmp')
                elif node.oper == ast_nodes.Oper.divide:
                    return self.builder.sdiv(left, right, 'divtmp')
                elif node.oper == ast_nodes.Oper.mod:
                    return self.builder.srem(left, right, 'modtmp')
                elif node.oper == ast_nodes.Oper.exponent:
                    powi = self.module.declare_intrinsic('llvm.powi', [type_dbl])
                    leftdbl = self.builder.sitofp(left, type_dbl, 'leftasdbl')
                    resdbl = self.builder.call(powi, [leftdbl, right], 'fcall')
                    return self.builder.fptosi(resdbl, type_i32)

            return(left)
        else:
            print("codegen not found: %s" % (type(node)))


