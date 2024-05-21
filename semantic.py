
import ast_nodes

types = ['int','real','char','string','boolean','void']

class Any(object):
	def __eq__(self,o):
		return True
	def __ne__(self,o):
		return False


# contexts has return value of function as name
class Context(object):
    def __init__(self,name=None, type=None):
        self.variables = {}
        self.var_count = {}
        self.name = name
        self.type = type
        if name != None:
            self.set_var(name.lower(), type)
	
    def has_var(self,name):
        return name in self.variables
	
    def get_var(self,name):
        return self.variables[name]
	
    def set_var(self,name,typ):
        self.variables[name] = typ
        self.var_count[name] = 0


typemap = {
}

def isreal(intype):
      return ((intype == "float") or (intype == "double"))

def totype(intype):
      if intype in typemap:
            return typemap[intype]
      else:
            return (intype)
      
# The is always the global context
contexts = [Context("global")]

functions = {
	'write':('void',[
			("a",Any())
		]),
	'writeln':('void',[
			("a",Any())
		]),
    'print_string':('void',[
			("a",'string')
		]),
	'print_int':('void',[
			("a",'int')
		]),
	'writereal':('void',[
			("a",'real')
		]),
	'writelnint':('void',[
			("a",'int')
		]),
	'writelnreal':('void',[
			("a",'real')
		])
}

def pop():
	count = contexts[-1].var_count
	for v in count:
		if count[v] == 0:
			print("Warning: variable %s was declared, but not used." % v)
	contexts.pop()

def check_if_function(var):
	if var.lower() in functions and not is_function_name(var.lower()):
		raise Exception( "A function called %s already exists" % var)
		
def is_function_name(var):
	for i in contexts[::-1]:
		if i.name == var:
			return True
	return False
		
		
def has_var(varn):
	var = varn.lower()
	check_if_function(var)
	for c in contexts[::-1]:
		if c.has_var(var):
			return True
	return False

def get_var(varn):
    var = varn.lower()
    for c in contexts[::-1]:
        if c.has_var(var):
            c.var_count[var] += 1
            return c.get_var(var)
    raise Exception( "Variable %s is referenced before assignment" % var)
	
def set_var(varn,typ):
	var = varn.lower()
	check_if_function(var)
	now = contexts[-1]
	if now.has_var(var):
		raise Exception("Variable %s already defined" % var )
	else:
		now.set_var(var,typ)
	
def get_params(node):
	if node.XXXXX == "parameter":
		return [check(node.args[0])]
	else:
		l = []
		for i in node.args:
			l.extend(get_params(i))
		return l
		
def flatten(n):
	if not is_node(n): return [n]
	if not n.type.endswith("_list"):
		return [n]
	else:
		l = []
		for i in n.args:
			l.extend(flatten(i))
		return l

def sem_arglist(args):
	if isinstance(args, ast_nodes.ValVarDeclaration):
		if isinstance(args.type, ast_nodes.ArrayExp):
			return sem_arglist(args.type)
		else:
			return totype(args.type)
	elif isinstance(args, ast_nodes.ArrayExp):
		return [sem_arglist(args.type)]
	else:
		return totype(args)
		
		 

def is_node(n):
    return isinstance(n, ast_nodes.ASTNode)

def check(node, target_basic_type=None):
      if not is_node(node):
            if hasattr(node,"__iter__") and type(node) != type(""):
                  for i in node:
                        check(i, target_basic_type)
            else:
                  print("returning node")
                  return node
      else:
            if isinstance(node, ast_nodes.ExpressionList):
                print(node)
                print(f"checking for {target_basic_type}")
                last = None
                returntype = None
                vallist = []
                same = False
                for n in node.expr_list:
                    new_type=check(n, target_basic_type)
                    if last == None:
                          last = new_type
                          same = True
                    else:
                          if last != new_type:
                                same = False
                    vallist = vallist + [new_type]
                    returntype = last
                print(vallist)
                if same and len(vallist) > 1:
                      # all expressions in list are the same and there are multiple expressions -> array
                      returntype = [returntype]
                print(returntype)
                return returntype

            elif isinstance(node, ast_nodes.ValVarDeclaration):
                print(node)
                var_name = node.name
                var_type = sem_arglist(node.type)
                basictype=var_type
                while isinstance(basictype, list):
                    basictype = basictype[0]
                print(f"basictype {basictype}")
                print(f"ValVarDeclaration {var_name} : {var_type}")
                set_var(var_name, var_type)
                if node.value != None:
                      init_val_type = check(node.value, basictype)
                      if init_val_type != var_type:
                            raise Exception("var %s (%s) is not the same type as inital value: %s (%s)" % (var_name, var_type, init_val_type, node.value))

            elif isinstance(node, ast_nodes.FunctionCall):
                print(node)
                fun_name = node.name
                if not fun_name.lower() in functions:
                      raise Exception("Function %s (%s) is not in function list" % (fun_name, fun_name.lower()))
                funinfo=functions[fun_name.lower()]
                print(f"function call: {funinfo}")
                fun_type = funinfo[0]
                fun_args = funinfo[1]
                print(f"function {fun_name}: {fun_type} <{fun_args}>")
                # Check arguments
                print(len(fun_args))
                if node.args == None:
                    raise Exception("function call needs args")
                if isinstance(node.args, ast_nodes.EmptyExp):
                    if len(fun_args) != 0:
                        raise Exception("Function %s needs argumetns (%s)" % (fun_name, node.args))
                else:
                    if len(fun_args) != len(node.args.expr_list):
                        raise Exception("Function Number of arguments %s (%s)" % (len(fun_args), len(node.args.expr_list)))
                    for i in range(len(fun_args)):
                        lt = fun_args[i][1]
                        rt = check(node.args.expr_list[i])
                        if lt != rt:
                              raise Exception("Function arguments (%s) do not match %s != %s" % (i, lt, rt))
                return fun_type

            elif isinstance(node, ast_nodes.FunctionDec):
                fun_name = node.name
                fun_type = sem_arglist(node.return_type)
                check_if_function(fun_name)
                args = []
                for i in node.params.args:
					# TODO: args are also variables
                    #print("var %s, %s, %s", (i, i.name, i.type))
                    #print(sem_arglist(i))
                    if isinstance(i, ast_nodes.EmptyExp):
                          continue
                    args = args + [[i.name, sem_arglist(i)]]
                functions[fun_name.lower()] = (fun_type,args)
                contexts.append(Context(fun_name, fun_type))
                print(f"fun: {fun_name}: {fun_type}")
				# fun: subtractUntilNegative2D: ['int']
                print(args)
				# [['array2D', [['int']]], ['numRows', 'int'], ['numCols', 'int']]
                for i in args:
                    set_var(i[0],i[1])
                check(node.body)
                pop()

            elif isinstance(node, ast_nodes.OpExp):
                op = node.oper
                vt1 = check(node.left, target_basic_type)
                vt2 = check(node.right, target_basic_type)
                if op == ast_nodes.Oper.notop:
                      if vt2 != 'boolean':
                        raise Exception("Arguments of operation '%s' must be boolean got %s." % (op, vt2))
                      return vt2
                if op in [ast_nodes.Oper.plus, ast_nodes.Oper.minus,
                          ast_nodes.Oper.times, ast_nodes.Oper.divide]:
                    if vt1 != 'int' and not isreal(vt1):
                        raise Exception("Operation %s requires numbers." % op)
                    if vt2 != 'int' and not isreal(vt2):
                        raise Exception("Operation %s requires numbers." % op)
                    if vt1 == 'int':
                          return vt2
                    else:
                          return vt1
                if op == ast_nodes.Oper.divide:
                    if not isreal(vt1):
                        raise Exception("Operation %s requires float or double." % op)
                if vt1 != vt2:
                    print(node)
                    raise Exception("Arguments of operation '%s' must be of the same type. Got %s and %s." % (op,vt1,vt2))
                if op == ast_nodes.Oper.mod:
                    if vt2 != 'int' or vt1 != 'int':
                        raise Exception("Operation %s int." % op)
                if op in [ast_nodes.Oper.lt, ast_nodes.Oper.gt,
                          ast_nodes.Oper.ge, ast_nodes.Oper.le,
                            ast_nodes.Oper.eq, ast_nodes.Oper.neq ]:
                    return 'boolean'
                else:
                    #print("return %s" % (vt1))
                    return vt1    

            elif isinstance(node, ast_nodes.WhileExp):
                #print(node.test)
                test_type = check(node.test)
                if test_type != 'boolean':
                        raise Exception("%s condition requires a boolean. Got %s instead." % ("While",test_type))
                check(node.body)

            elif isinstance(node, ast_nodes.IfExp):
                test_type = check(node.test)
                if test_type != 'boolean':
                        raise Exception("%s condition requires a boolean. Got %s instead." % ("If",test_type))
                check(node.then_do)
                if node.else_do != None:
                      check(node.else_do)

            elif isinstance(node, ast_nodes.ArrayExp):
                    if isinstance(node.type, ast_nodes.FunctionCall):
                        ret_type = check(node.type)
                    else:
                        ret_type = get_var(node.type)
                    if node.size != None:
                        # Index is an expression list a[1][2]
                        for exp in node.size.expr_list:
                            exp_type = check(exp)
                            if exp_type != 'int':
                                raise Exception("Array Index must be integer. Got %s (%s) instead." % (exp_type, exp))
                            ret_type = ret_type[0]
                    return ret_type

            elif isinstance(node, ast_nodes.VarExp):
                  #print(f"VarExp: {node}")
                  #print("VarExp: type: ", get_var(node.var))
                  return get_var(node.var)

            elif isinstance(node, ast_nodes.AssignExp):
                  #print(f"AssignExp: {node}")
                  lt = check(node.var)
                  rt = check(node.exp)
                  print(f"AssignExp: left = {lt} right = {rt} ")
                  return lt

            elif isinstance(node, ast_nodes.IntExp):
                  if target_basic_type in ["float", "double"]:
                        return target_basic_type
                  return "int"

            elif isinstance(node, ast_nodes.FloatExp):
                if target_basic_type in ["double"]:
                        return target_basic_type
                return "float"

### TODO           elif isinstance(node, ast_nodes.DoubleExp):
### TODO                return "double"

            elif isinstance(node, ast_nodes.BoolExp):
                  return "boolean"

            elif isinstance(node, ast_nodes.StringExp):
                  return "string"

            elif isinstance(node, ast_nodes.EmptyExp):
                  return None

            else:
                print( "semantic missing:", type(node))	

'''
#Todo
# not used ValueDec
# not used VariableDec
# AssignExp
# EmptyExp
ValVarList
#FunctionCall
'''

'''
#Unused DataTypes
#DeclarationBlock
#Field
#RecordTy
#ArrayTy
#ValExp
#NilExp
#ValDeclaration
#VarDeclaration
#VarList
#ValList
'''
