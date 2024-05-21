import ast_nodes1

types = ['integer','real','char','string','boolean','void']

class Any(object):
	def __eq__(self,o):
		return True
	def __ne__(self,o):
		return False

class Context(object):
	def __init__(self,name=None):
		self.variables = {}
		self.var_count = {}
		self.name = name
	
	def has_var(self,name):
		return name in self.variables
	
	def get_var(self,name):
		return self.variables[name]
	
	def set_var(self,name,typ):
		self.variables[name] = typ
		self.var_count[name] = 0

typemap = {
      "int": 'integer',
      "float": 'real'
}
def totype(intype):
      if intype in typemap:
            return typemap[intype]
      
# The is always the global context
contexts = [Context("global")]

functions = {
	'write':('void',[
			("a",Any())
		]),
	'writeln':('void',[
			("a",Any())
		]),
	'writeint':('void',[
			("a",'integer')
		]),
	'writereal':('void',[
			("a",'real')
		]),
	'writelnint':('void',[
			("a",'integer')
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
	raise Exception( "Variable %s is referenced before assignment" )% var
	
def set_var(varn,typ):
	var = varn.lower()
	check_if_function(var)
	now = contexts[-1]
	if now.has_var(var):
		raise Exception( "Variable %s already defined") % var
	else:
		now.set_var(var,typ.lower())
	
def get_params(node):
	if node.type == "parameter":
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
		

def is_node(n):
	return hasattr(n,"type")

def check(node):
	if not is_node(node):
		if hasattr(node,"__iter__") and type(node) != type(""):
			for i in node:
				check(i)
		else:
			return node
	else:
            if node.XXXXX in ['identifier']:
                return node.args[0]
            elif node.XXXXX in ['var_list','statement_list','function_list']:
                return check(node.args)
            elif isinstance(node, ast_nodes1.ExpressionList):
                  return check(node.expr_list)
            elif node.XXXXX in ["program","block"]:
                contexts.append(Context())
                check(node.args)
                pop()
            elif isinstance(node, ast_nodes1.VarDeclaration):
                var_name = node.name
                var_type = totype(node.type)
                set_var(var_name, var_type)
                if node.initial_value != None:
                      init_val_type = check(node.initial_value)
                      if init_val_type != var_type:
                            raise Exception("var %s (%s) is not the same type as inital value: %s" % (var_name, var_type, init_val_type))
                
            elif node.XXXXX in ['function','procedure']:
                head = node.args[0]
                name = head.args[0].args[0].lower()
                check_if_function(name)
                if len(head.args) == 1:
                    args = []
                else:
                    args = flatten(head.args[1])
                    args = map(lambda x: (x.args[0].args[0],x.args[1].args[0]), args)
                if node.XXXXX == 'procedure':
                    rettype = 'void'
                else:
                    rettype = head.args[-1].args[0].lower()
                functions[name] = (rettype,args)
                contexts.append(Context(name))
                for i in args:
                    set_var(i[0],i[1])
                check(node.args[1])
                pop()
            elif node.XXXXX in ["function_call"]:
                fname = node.args[0].args[0].lower()
                if fname not in functions:
                    raise Exception("Function %s is not defined" % fname)
                if len(node.args) > 1:
                    args = get_params(node.args[1])
                else:
                    args = []
                rettype,vargs = functions[fname]
                if len(args) != len(vargs):
                    raise Exception("Function %s is expecting %d parameters and got %d" % (fname, len(vargs), len(args)))
                else:
                    for i in range(len(vargs)):
                        if vargs[i][1] != args[i]:
                            raise Exception("Parameter #%d passed to function %s should be of type %s and not %s" % (i+1,fname,vargs[i][1],args[i]))
                return rettype
            elif node.XXXXX in ['assign',':=']:    
                    varn = check(node.args[0]).lower()
                    if is_function_name(varn):
                        vartype = functions[varn][0]
                    else:
                        if not has_var(varn):
                            raise Exception("Variable %s not declared" % varn)
                        vartype = get_var(varn)
                    assgntype = check(node.args[1])
                    if vartype != assgntype:
                        raise Exception("Variable %s is of type %s and does not support %s" % (varn, vartype, assgntype))
            elif node.XXXXX in ['&&','||']:
                op = node.args[0].args[0]
                for i in range(1,2):
                    a = check(node.args[i])
                    if a != "boolean":
                        raise Exception("%s requires a boolean. Got %s instead." % (op,a))
            elif isinstance(node, ast_nodes1.OpExp):
                op = node.oper
                vt1 = check(node.left)
                vt2 = check(node.right)
                if vt1 != vt2:
                    raise Exception("Arguments of operation '%s' must be of the same type. Got %s and %s." % (op,vt1,vt2))
                if op in [ast_nodes1.Oper.plus, ast_nodes1.Oper.minus,
                          ast_nodes1.Oper.times, ast_nodes1.Oper.divide]:
                    if vt1 != 'integer':
                        raise Exception("Operation %s requires integers." % op)
                if op == ast_nodes1.Oper.divide:
                    if vt1 != 'real':
                        raise Exception("Operation %s requires reals." % op)
                if op in [ast_nodes1.Oper.lt, ast_nodes1.Oper.gt,
                          ast_nodes1.Oper.ge, ast_nodes1.Oper.le,
                            ast_nodes1.Oper.eq, ast_nodes1.Oper.neq ]:
                    return 'boolean'
                else:
                    return vt1    
            elif node.XXXXX in ['if','while','repeat','elif']:
                if node.XXXXX == 'repeat':
                    c = 1
                else:
                    c = 0
                t = check(node.test)
                if t != 'boolean':
                    raise Exception("%s condition requires a boolean. Got %s instead." % (node.XXXXX,t))
                # check body
                check(node.then_do)
                # check else
                if node.else_do != None:
                    check(node.else_do)
            elif isinstance(node, ast_nodes1.WhileExp):
                test_type = check(node.test)
                if test_type != 'boolean':
                        raise Exception("%s condition requires a boolean. Got %s instead." % ("While",test_type))
                check(node.body)
            elif isinstance(node, ast_nodes1.IfExp):
                test_type = check(node.test)
                if test_type != 'boolean':
                        raise Exception("%s condition requires a boolean. Got %s instead." % ("If",test_type))
                check(node.then_do)
                if node.else_do != None:
                      check(node.else_do)
        
            elif node.XXXXX == '!':
                return check(node.args[0])
            elif isinstance(node, ast_nodes1.IntExp):
                  return "integer"
            elif isinstance(node, ast_nodes1.FloatExp):
                  return "float"
 ### TODO           elif isinstance(node, ast_nodes.DoubleExp):
 ### TODO                return "float"
            elif isinstance(node, ast_nodes1.BoolExp):
                  return "boolean"
            elif isinstance(node, ast_nodes1.StringExp):
                  return "string"
            elif node.XXXXX == "element":
                if node.type == 'identifier':
                    return get_var(node.args[0].args[0])
                elif node.type == 'function_call_inline':
                    return check(node.args[0])
                else:
                    return check(node.args[0])
            else:
                print( "semantic missing:", type(node))	
