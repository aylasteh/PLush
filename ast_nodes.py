from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ASTNode(ABC):
    position: int

    def pp(self) -> str:
        return('"position": ' + f"{self.position}")

class Declaration(ASTNode):
    pass

    def pp(self) -> str:
        ret = '"Declaration": "basic type"'

class Type(ASTNode):
    pass

    def pp(self) -> str:
        ret = '"Type": "basic type"'


class Expression(ASTNode):
    pass

    def pp(self) -> str:
        ret = '"Expression": "basic type"'

@dataclass
class ExpressionList(ASTNode):
    expr_list: [Expression]

    def pp(self) -> str:
        ret = '"ExpressionList": { "position":' + f"  {self.position}, "
        ret = ret + '"expr_list": ['
        a = [ "{" + i.pp() + "}" for i in self.expr_list]
        ret = ret + ','.join(a)
        ret = ret + "]"
        ret = ret + "}"
        return ret


class Variable(ASTNode):
    pass

    def pp(self) -> str:
        ret = '"Variable": "basic type"'

class Oper(Enum):
    plus = 1
    minus = 2
    times = 3
    divide = 4
    eq = 5
    neq = 6
    lt = 7
    le = 8
    gt = 9
    ge = 10
    exponent = 11
    andop = 12
    orop = 13
    mod = 14
    notop = 15

    def pp(self) -> str:
        ret = '"Oper": {'
        ret = ret + '"'+ f"{self.name}" + '":' + f"{self.value}"
        ret = ret + "}"
        return ret


# DECLARATION


@dataclass
class DeclarationBlock(ASTNode):
    declaration_list: List[Declaration]
    dimension: List[int]

    def pp(self) -> str:
        ret = '"DeclarationBlock": { "declaration_list": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"declaration_list": ['
        a = [ "{" + i.pp() + "}" for i in self.declaration_list]
        ret = ret + ','.join(a)
        ret = ret + "],"
        ret = ret + '"dimension" : ['
        ret = ret + ",".join(str(i) for i in self.dimension)
        ret = ret + "]"
        ret = ret + "}"
        ret = ret + "}"
        return ret

# EXPRESSION

@dataclass
class VarExp(Expression):
    var: Variable
    sem_type: str = None

    def pp(self) -> str:
        ret = '"VarExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"var" : "' + f"{self.var}" + '",'
        ret = ret + '"sem_type": "'
        if self.sem_type != None:
            ret = ret + f"{self.sem_type}"
        ret = ret + '"'
        ret = ret + "}"
        return ret

@dataclass
class BoolExp(Expression):
    value: bool

    def pp(self) -> str:
        ret = '"BoolExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"value" : "' + f"{self.value}" + '"'
        ret = ret + "}"
        return ret

@dataclass
class FloatExp(Expression):
    value: float

    def pp(self) -> str:
        ret = '"FloatExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"value" : ' + f"{self.value}"
        ret = ret + "}"
        return ret

@dataclass
class IntExp(Expression):
    int: int
    sem_type: str = None

    def pp(self) -> str:
        ret = '"IntExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"int" : ' + f"{self.int},"
        ret = ret + '"sem_type": "'
        if self.sem_type != None:
            ret = ret + f"{self.sem_type}"
        ret = ret + '"'
        ret = ret + "}"
        return ret

@dataclass
class StringExp(Expression):
    string: str

    def pp(self) -> str:
        ret = '"StringExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"string" : "' + self.string + '"'
        ret = ret + "}"
        return ret


@dataclass
class AssignExp(Expression):
    var: Variable
    exp: Expression

    def pp(self) -> str:
        ret = '"AssignExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"var" : {' + self.var.pp() + "},"
        ret = ret + '"exp" : {' + self.exp.pp() + "}"
        ret = ret + "}"
        return ret

@dataclass
class IfExp(Expression):
    test: Expression
    then_do: ExpressionList
    else_do: Optional[ExpressionList]

    def pp(self) -> str:
        ret = '"IfExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"test" : {' + self.test.pp() + "},"
        ret = ret + '"then_do" : {' + self.then_do.pp() + "},"
        ret = ret + '"else_do": {'
        if self.else_do != None:
            ret = ret + self.else_do.pp()
        ret = ret + "}"
        ret = ret + "}"
        return ret


@dataclass
class WhileExp(Expression):
    test: Expression
    body: ExpressionList

    def pp(self) -> str:
            ret = '"WhileExp": {'
            ret = ret + '"position" : ' + f" {self.position}, "
            ret = ret + '"test" : {' + self.test.pp() + "},"
            ret = ret + '"body" : {' + self.body.pp() + "}"
            ret = ret + "}"
            return ret


@dataclass
class ArrayExp(Expression):
    type: str
    size: Expression
    init: Expression

    def pp(self) -> str:
        ret = '"ArrayExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"type" : "' + f"{self.type}" '",'
        ret = ret + '"size" : {'
        if self.size != None:
            ret = ret + self.size.pp()
        ret = ret + "},"
        ret = ret + '"init" : {'
        if self.init != None:
            ret = ret + self.init.pp()
        ret = ret + "}"
        ret = ret + "}"
        return ret


@dataclass
class EmptyExp(Expression):
    pass

    def pp(self) -> str:
        ret = '"EmptyExp": {' + '"position" : ' + f" {self.position} " + '}'
        return ret  

@dataclass
class OpExp(Expression):
    oper: Oper
    left: Expression
    right: Expression
    opt : int = None
    sem_type: str = None

    def pp(self) -> str:
        ret = '"OpExp": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"oper" : {' + self.oper.pp() +'},'
        ret = ret + '"left": {'
        if self.left != None:
            ret = ret + self.left.pp()
        ret = ret + '},'
        ret = ret + '"right": {'
        if self.right != None:
            ret = ret + self.right.pp()
        ret = ret + '}, '
        if self.opt != None:
            ret = ret + '"opt" : ' + f" {self.opt}, "
        else:
            ret = ret + '"opt" : {},'
        ret = ret + '"sem_type": "'
        if self.sem_type != None:
            ret = ret + f"{self.sem_type}"
        ret = ret + '"'
        ret = ret + "}"
        return ret

# VARIABLE


@dataclass
class ValVarDeclaration(Declaration):
    isval: bool
    name: str
    type: Type
    value: Expression
    dimension: List[int]
    complex_type: str = ""

    def pp(self) -> str:
        ret = '"ValVarDeclaration": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"name" : "' + f"{self.name}" + '", '
        if isinstance(self.type, ArrayExp):
            rret = ret + '"type" : {' + self.type.pp() + "}, "
        else:
            ret = ret + '"type" : "' + self.type + '",'
        
        ret = ret + '"value" : {'
        if self.value != None:
            ret = ret + '"value" : {' + self.value.pp() + "}"
        ret = ret + '},'
        ret = ret + '"dimension" : ['
        a = [ i for i in self.dimension]
        ret = ret + ','.join(str(i) for i in a)
        ret = ret + "],"
        ret = ret + '"complex_type" : "' + f"{self.complex_type}" + '"'
        ret = ret + "}"
        return ret

@dataclass
class ValVarList(ASTNode):
    args: List[ValVarDeclaration]

    def pp(self) -> str:
        ret = '"ValVarList": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"args" : ['
        a = [ "{" + i.pp() + "}" for i in self.args]
        ret = ret + ','.join(a)
        ret = ret + "]"
        ret = ret + "}"
        return ret


@dataclass
class FunctionDec(ASTNode):
    name: str
    params: ValVarList
    param_escapes: List[bool]
    return_type: Optional[str]
    body: ExpressionList
    arg_types: List[str]

    def pp(self) -> str:
        ret = '"FunctionDec": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"name": "' + self.name + '",'
        ret = ret + '"params" : {' + self.params.pp() + "},"
        ret = ret + '"body" : {'
        if self.body != None:
            ret = ret + self.body.pp()
        ret = ret + "}"
        ret = ret + "}"
        return ret

@dataclass
class ArgsList(ASTNode):
    args: List[DeclarationBlock]

    def pp(self) -> str:
        ret = '"ArgsList": {'
        ret = ret + '"position" : ' + f" {self.position},"
        ret = ret + '"args": ['
        a = [ "{" + i.pp() + "}" for i in self.args]
        ret = ret + ','.join(a)
        ret = ret + "]"
        ret = ret + "}"
        return ret
    
@dataclass
class FunctionCall(ASTNode):
    name: str
    args: ArgsList

    def pp(self) -> str:
        ret = '"FunctionCall": {'
        ret = ret + '"position" : ' + f" {self.position}, "
        ret = ret + '"name": "' + self.name + '",'
        ret = ret + '"args" : {' + self.args.pp() + "}"
        ret = ret + "}"
        return ret
